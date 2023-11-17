# Adjust channel priority on conda env
conda config --add channels bioconda
conda config --add channels conda-forge

# Install kraken2 via conda, for removing human reads
conda install -y -c bioconda kraken2

# Install samtools
conda install -y "samtools>=1.10"

# Install mafft
conda install -y -c bioconda mafft

# Install MASH
conda install -y -c bioconda mash

# # Download pre-built kraken2 database with human genome only
mkdir kraken2_human_db
curl -L -o kraken2_human_db/kraken2_human_db.tar.gz https://ndownloader.figshare.com/files/23567780
tar -xzvf kraken2_human_db/kraken2_human_db.tar.gz

# Download trimmomatic and extract
wget http://www.usadellab.org/cms/uploads/supplementary/Trimmomatic/Trimmomatic-0.39.zip
unzip Trimmomatic-0.39.zip
rm Trimmomatic-0.39.zip

# Download BWA
curl -L https://github.com/bwa-mem2/bwa-mem2/releases/download/v2.2.1/bwa-mem2-2.2.1_x64-linux.tar.bz2 | tar jxf -

# Install viral consensus tool
wget -qO- "https://github.com/samtools/htslib/releases/download/1.18/htslib-1.18.tar.bz2" | tar -xj
cd htslib-*
autoreconf -i
./configure
make
sudo make install
cd ..

git clone https://github.com/niemasd/ViralConsensus.git
cd ViralConsensus
make
cd ..
