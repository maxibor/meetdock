F90 = /usr/bin/gfortran
COMPILERDIR= /usr/bin
LIBS = -llapack
#---------------
OF=format_declaration.o\
   particles.o\
   run_parameter.o\
   proteins.o\
   springs.o\
   microb.o\
   Interface.o

FF=format_declaration.f90\
   particles.f90\
   run_parameter.f90\
   proteins.f90\
   springs.f90\
   microb.f90\
   interface.f90


main:	$(OF)
	$(COMPILERDIR)/gfortran $(OF) -o Interface.out

clean:  
	rm -f *.o *.kmo *.mod main 

format_declaration.o: format_declaration.f90
#	$(COMPILERDIR)/ifort $(PFLAGS) format_declaration.f90
	$(F90)  -c format_declaration.f90

Interface.o: Interface.f90 run_parameter.f90 format_declaration.f90\
             particles.f90 springs.f90 proteins.f90 microb.f90
#	$(COMPILERDIR)/ifort -free  $(PFLAGS) Interface.f90
	$(F90) -c Interface.f90

microb.o: microb.f90 particles.f90 run_parameter.f90
#	$(COMPILERDIR)/ifort -free  $(PFLAGS) microb.f90
	$(F90)  -c microb.f90

particles.o: particles.f90
#	$(COMPILERDIR)/ifort -free $(PFLAGS) particles.f90
	$(F90)  -c particles.f90

proteins.o: proteins.f90 run_parameter.f90 particles.f90\
            format_declaration.f90
#	$(COMPILERDIR)/ifort -free $(PFLAGS) proteins.f90 
	$(F90)  -c proteins.f90

run_parameter.o: run_parameter.f90 format_declaration.f90
#	$(COMPILERDIR)/ifort -free  $(PFLAGS) run_parameter.f90
	$(F90)  -c run_parameter.f90

springs.o: springs.f90 run_parameter.f90 particles.f90\
           format_declaration.f90
#	$(COMPILERDIR)/ifort -free  $(PFLAGS) springs.f90
	$(F90)  -c springs.f90
