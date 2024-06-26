import subprocess as sp
import argparse 
from app.src.preprocess import run_kraken
from app.src.trim_adapters import run_trim
from app.src.map_reads_to_ref import run_map
from app.src.generate_counts import run_counts
from app.src.post_filter import run_post_filter

class E2eRunner:
    '''Complete pipeline using functionality of original scripts. See Readme from original repo.
    Note: several optional arguments from original are hard-coded, especially on step "analysis".
    Full functionality offered by API.
    '''
    def __init__(self) -> None:
        self.a       = self.parse_args()
        self.aliases = self.initiate_aliases()

    def shell(self, args, executable='/bin/bash'):
        '''Call Bash shell with input string as argument'''
        sp.run(args, text=True,shell=True, executable=executable)

    def initiate_aliases(self):
        '''Load aliases for shell cmds'''
        aliases = {}
        aliases["trim"] = 'java -jar ./Trimmomatic-0.39/trimmomatic-0.39.jar'
        aliases["bwa"]  = './bwa-mem2-2.2.1_x64-linux/bwa-mem2'
        return aliases

    def parse_args(self):
        '''Parse command-line arguments'''
        p = argparse.ArgumentParser(description=__doc__, epilog='Complete pipeline using functionality of original scripts')
        p.add_argument( '-ExpDir',  default="data/",  required=True,   help='Provide directory for input data' )
        p.add_argument( '-SeqName', default=None,     required=True,   help='Provide input sequence (experiment) name.' )
        p.add_argument( '-ExpName', default='myexp',  required=False,  help='Name your experiment batch.' )
        p.add_argument( '-AdaptP',  default="Trimmomatic-0.39/adapters/all.fa", required=False, help='Location of your Trimmomatic adapter sequences - usually in Trimmomatic path.' )
        p.add_argument( '-RefStem', default="",       required=False,  help="Path to mapping file (fasta)")
        p.add_argument( '-PostFilt',default=False,    required=False,  help="Filter BAM file to remove reads marked as contamination")
        p.add_argument( '-Samples',                   required=True,   help="CSV file containing sample information. Absolute path required")
        p.add_argument( '-Probes',  default="",       required=False,  help="CSV file containing probe length mappings. Absolute path required")
        return p.parse_args()
    
    def main(self):
        '''Entrypoint'''
        self.initiate_aliases()
        run_kraken(self.a, api_entry=False)
        self.shell(f"python3 -m app.src.filter_keep_reads -i {self.a.ExpDir}{self.a.SeqName}_[12].fastq.gz -k {self.a.ExpDir}{self.a.SeqName}_1.kraken --xT Homo,Alteromonas,Achromobacter -x 1969841 --lineage data/ncbi_lineages_2023-06-15.csv.gz")
        run_trim(self.a, trim_path=self.aliases["trim"], api_entry=False)
        run_map(self.a, bwa_path=self.aliases["bwa"], api_entry=False)
        run_counts(self.a, api_entry=False)
        self.shell(f"python3 src/process_pool_grp.py -i {self.a.ExpDir}PosCounts.csv --samples {self.a.Samples} -p {self.a.Probes} -b {self.a.ExpName}")
        if self.a.PostFilt:
            run_post_filter(self.a, api_entry=False)

if __name__ == "__main__":
    '''Example input
    python3 -m app.end_to_end_script -ExpDir data/ -SeqName ERR10812890 -RefStem rmlst_virus_extra_ercc_2018.fasta -PostFilt True -Samples data/samples.csv -Probes data/probelengths_rmlst_virus_extra_ercc.csv
    '''
    cls = E2eRunner()
    cls.main()
