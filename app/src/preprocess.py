from app.utils.shell_cmds import shell
from app.utils.error_handlers import error_handler_cli
from app.utils.utility_fns import enumerate_read_files
from app.utils.system_messages import end_sec_print
from app.utils.shell_cmds import stoperr
import os


def run_kraken(p):
    '''Call Kraken2 to remove unwanted reads'''
    p["SeqNames"] = enumerate_read_files(p["ExpDir"])
    out_fnames = [f'{p["SaveDir"]}/{p["ExpName"]}/{p["ExpName"]}.kraken',
                  f'{p["SaveDir"]}/{p["ExpName"]}/kraken_report.tsv']
    for ofn in out_fnames:
        '''Kill existing kraken files if present'''
        if os.path.exists(ofn):
            os.remove(ofn)
    out = shell(
        f'kraken2 --db {p["KrakenDbDir"]} --paired --threads {p["NThreads"]} --output {out_fnames[0]} --report {out_fnames[1]} {p["SeqNames"][0]} {p["SeqNames"][1]}', is_test=True)
    '''Test for success'''
    error_handler_cli(out, out_fnames[1], "kraken")
    end_sec_print(f"Kraken2 annotations complete")
