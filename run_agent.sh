#while true;
#do
#cd /mnt/data1/2024/01/15/lang_agent/
cd /lang_agent/
dune exec bin/scanner.exe -- -c .txt -x .test  \
    -s  $1 \
    -p  $5 \
    "$3" \
    -m $4 \
    -u $2

    
#done;
