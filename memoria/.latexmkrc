# Configuración de latexmk (la usan Makefile, la CI, VS Code y la terminal)
$pdf_mode = 1;                 # pdflatex
$pdflatex = 'pdflatex -interaction=nonstopmode -halt-on-error -file-line-error -synctex=1 %O %S';
$bibtex_use = 2;               # ejecuta biber cuando haga falta y limpia el .bbl
$max_repeat = 6;
$clean_ext = 'bbl run.xml synctex.gz lol loa nav snm vrb';
