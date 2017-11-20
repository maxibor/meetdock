#!/bin/csh

set PROTDIR = ../../Proteins #pdb_files

#conformations to build 
foreach DOCKPOS (1)

# to specify the pdb to build (receptor) (Here, only the pdb 1TMQ_l_u will be considered as receptor)
foreach PROT (3NHE_A.pdb)
set PROT1 = ${PROT:t:r}

set PROTid1 = `echo {$PROT1:r}| cut -c 1-6`
set PROTroot = `echo {$PROT1:r}| cut -c 1-4`
set minroot = `echo $PROTroot |tr "[A-Z]" "[a-z]"`

# to specify the pdb to build (ligand) (Here, only the pdb 1TMQ_r_u will be considered as ligand)
foreach PROTT (3NHE_B.pdb)
set PROT2 = ${PROTT:t:r}
set PROTid2 = `echo {$PROT2:r}| cut -c 1-6`

rm proteins.dat


echo "'"$PROTDIR/$PROT1.pdb"'">proteins.dat
echo "'"$PROT1"'">>proteins.dat
echo "'"$PROTDIR/$PROT2.pdb"'">>proteins.dat
echo "'"$PROT2"'">>proteins.dat
echo "'selection'">>proteins.dat
echo "$DOCKPOS">>proteins.dat

# builing 3D coords for the LIG from phi, theta, alpha, beta, gamma and REC coords
../progs_builder/Interface.out 

end
end
end



