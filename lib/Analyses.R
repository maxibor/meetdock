#Analyse des scores obtenus des complexes par l'utilisation de FoldX
library(MASS)
scores = read.csv('./Outputs/resultats.csv', header = F)[,1]
truehist(scores)
mean(scores)
dev.copy2pdf(file = './Outputs/resultats.pdf')
dev.off()
