#!/bin/bash

rm -rf studentsource/
mkdir studentsource

for i in {0..6}; do
    mkdir studentsource/Lab$i
    cp *.tex studentsource/Lab$i/
    cp -R images studentsource/Lab$i/
    cp -R Lab$i studentsource/Lab$i/
    rm -rf studentSource/Lab$i/Lab$i/solutions/*
    if [ $i -ne 0 ]; then
         rm -rf studentSource/Lab$i/Lab$i/traces/*
    fi
    cd studentsource/Lab$i/Lab$i
    rm -rf lab$i.pdf
    pdflatex  -synctex=1 -interaction=nonstopmode -file-line-error -recorder -output-directory="."  "lab$i.tex"
    # run a second time to get the acronyms right
    pdflatex  -synctex=1 -interaction=nonstopmode -file-line-error -recorder -output-directory="."  "lab$i.tex"
    rm -rf *.aux *latexmk *.fls *.log *.out *.synctex.gz
    cd ../../
    zip -r lab$i.zip Lab$i
    rm -rf Lab$i
    cd ..
done
