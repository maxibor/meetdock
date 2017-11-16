rm(list=ls())

library(optparse)

option_list = list(
  make_option(c("-f", "--file"), type="character", default="example.txt",
              help="File containing phi/theta coordinates of ligand positions around receptor.\n 
              Phi coordinates must be in first columns, theta coordinates in second example (see example.txt)",
              metavar="character")
);
opt_parser = OptionParser(option_list=option_list);
opt = parse_args(opt_parser);
input = opt$file
filename = basename(input)
filenamenoext = strsplit(filename, "\\.")[[1]][1]

# Retrieving receptor and ligand name (file name should begin by type XXXX_Y_WWWW_Z, XXXX being pdb id and Y chain id.)
rec_name = substr(input, 1, 6)
lig_name = substr(input, 8, 13)


if (opt$file == "example.txt") {
  pdf("example_map.pdf")
  titleplot = paste("ligand positions on receptor surface\nexample")
} else {
  pdf(paste0(filenamenoext,"_sampling_map.pdf"))
  titleplot = paste("ligand starting orientations on receptor surface\ninput file:", filename)
}

# Read the input file.
data = read.table(input, fill = TRUE, header = TRUE)

# Computing new coordinates after sinusoidal projection (Coordinates must be in radian) and plotting them.
ordinate = (data[,1])*cos(data[,2])*180/pi
abscissa = (data[,2])*180/pi
par(mar=c(11,5,9,2))
plot(ordinate,abscissa, col="red3", pch=20, cex=0.7,
     axes = FALSE,
     main = titleplot,
     frame.plot = TRUE,
     xlim = c(-180, 180), ylim = c(-90, 90),
     xlab = expression(paste(phi, " sin(", theta, ")")),
     ylab = expression(theta))
axis(1, at = seq(-180, 180, by = 90))
axis(2, at = seq(-90, 90, by = 45))
dev.off()