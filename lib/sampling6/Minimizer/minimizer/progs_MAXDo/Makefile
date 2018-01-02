F90 = /usr/bin/gfortran
COMPILERDIR= /usr/bin
LIBS = -llapack -lblas
FFLAGS= -c -g 
FFLAGS2= -c -march=native -ffast-math 
FFLAGS1= -march=native -ffast-math 

OF=timing.o\
   random.o\
   particles.o\
   format_declaration.o\
   eigen90.o\
   run_parameter.o\
   compute_distance.o\
   korobov.o\
   microb.o\
   proteins.o\
   constrain.o\
   zacharias.o\
   lj_red.o\
   born.o\
   springs.o\
   energa.o\
   cl_mc11a.o\
   cl_minfor.o\
   getmin.o\
   lanczos_pro.o\
   saddle_converge_pro.o\
   find_saddle_pro.o\
   art_pro.o\
   mapping.o\
   simulmain.o

main:	$(OF)
	$(COMPILERDIR)/gfortran $(FFLAGS1) $(OF) -o simulmain.out $(LIBS)

clean:  
	rm -f *.o *.kmo *.mod *.il main a

art_pro.o: art_pro.f90 particles.f90 run_parameter.f90 find_saddle_pro.f90\
           energa.f90 format_declaration.f90 random.f90 getmin.f90
	$(F90) $(FFLAGS) art_pro.f90

born.o: born.f90 particles.f90 compute_distance.f90 run_parameter.f90
	$(F90) $(FFLAGS) born.f90

compute_distance.o: compute_distance.f90 run_parameter.f90
	$(F90) $(FFLAGS) compute_distance.f90

constrain.o: constrain.f90 run_parameter.f90 particles.f90
	$(F90) $(FFLAGS) constrain.f90

energa.o: energa.f90 particles.f90 run_parameter.f90  microb.f90\
          lj_red.f90 born.f90 constrain.f90
	$(F90) $(FFLAGS) energa.f90

eigen90.o: eigen90.f90 particles.f90
	$(F90) $(FFLAGS) eigen90.f90

find_saddle_pro.o: find_saddle_pro.f90 saddle_converge_pro.f90\
                   random.f90 run_parameter.f90
	$(F90) $(FFLAGS) find_saddle_pro.f90  

format_declaration.o: format_declaration.f90
	$(F90) $(FFLAGS) format_declaration.f90

getmin.o: getmin.f90 run_parameter.f90 particles.f90 proteins.f90\
          microb.f90 springs.f90 energa.f90 cl_minfor.f90 timing.f90
	$(F90) $(FFLAGS) getmin.f90

korobov.o: korobov.f90 run_parameter.f90 particles.f90 compute_distance.f90
	$(F90) $(FFLAGS) korobov.f90

lanczos_pro.o: lanczos_pro.f90 run_parameter.f90 particles.f90\
               random.f90 energa.f90
	$(F90) $(FFLAGS) lanczos_pro.f90

lj_red.o: lj_red.f90 particles.f90 compute_distance.f90 run_parameter.f90 
	$(F90) $(FFLAGS) lj_red.f90

mapping.o: mapping.f90 run_parameter.f90 particles.f90 getmin.f90\
           korobov.f90
	$(F90) $(FFLAGS) mapping.f90

cl_mc11a.o: cl_mc11a.f90 particles.f90 
	$(F90) $(FFLAGS) cl_mc11a.f90

microb.o: microb.f90 run_parameter.f90 particles.f90
	$(F90) $(FFLAGS) microb.f90

cl_minfor.o: cl_minfor.f90 particles.f90 energa.f90 cl_mc11a.f90
	$(F90) $(FFLAGS) cl_minfor.f90

simulmain.o: simulmain.f90 run_parameter.f90 particles.f90 proteins.f90\
         timing.f90 springs.f90 zacharias.f90 mapping.f90
	$(F90) $(FFLAGS) simulmain.f90

particles.o: particles.f90 
	$(F90) $(FFLAGS) particles.f90

proteins.o: proteins.f90 particles.f90 run_parameter.f90 format_declaration.f90
	$(F90) $(FFLAGS) proteins.f90

run_parameter.o: run_parameter.f90 format_declaration.f90 particles.f90
	$(F90) $(FFLAGS) run_parameter.f90

saddle_converge_pro.o: saddle_converge_pro.f90 particles.f90\
                       run_parameter.f90 energa.f90 lanczos_pro.f90
	$(F90) $(FFLAGS) saddle_converge_pro.f90

timing.o: timing.f90
	$(F90) $(FFLAGS) timing.f90 -o timing.o

random.o: random.f90
	$(F90) $(FFLAGS) random.f90 -o random.o

springs.o: springs.f90 particles.f90 run_parameter.f90 format_declaration.f90
	$(F90) $(FFLAGS) springs.f90

zacharias.o: zacharias.f90 particles.f90 format_declaration.f90 run_parameter.f90
	$(F90) $(FFLAGS) zacharias.f90
