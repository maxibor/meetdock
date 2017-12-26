Program Get_receptor_area

use particles
use zacharias
use run_parameter
use format_declaration

  implicit none

  integer :: i
  integer :: Npositions,Npart

  real(8) :: xi,yi,zi
  real(8) :: xc,yc,zc
  real(8) :: ri,r_2,rci
  real(8) :: PtDens
 
  prot_id(1)%Pstot_number=0
  prot_id(1)%Ca_number=0
  allocate(prot_id(1)%Pstot_item(N_part_max))
  allocate(prot_id(1)%Ca_item(N_part_max))

  open(6,file='output.dat')
  open(20,file='proteins.dat',status='old')
  open(21,file='density.dat',status='old')
  open(22,file='input.dat',status='old',position='append') 

  N_protein=1
  prot_id(1)%radius=0.d0
  center(1)%x=0.d0
  center(1)%y=0.d0
  center(1)%z=0.d0

  side_x=1.d0
  side_y=1.d0
  side_z=1.d0

  read(21,*) PtDens
  write(6,form_tens) 'Points density around receptor (A-2): ',PtDens
  close(21)
  read(20,*) protein_file(1)
  write(6,*) 'Receptor file', protein_file(1)
  close(20) 
  call make_model
  
  do i=1,N_particle
    center(1)%x=center(1)%x+molecule(i)%x
    center(1)%y=center(1)%y+molecule(i)%y
    center(1)%z=center(1)%z+molecule(i)%z
  end do

  xc=center(1)%x/real(N_particle)  
  yc=center(1)%y/real(N_particle)  
  zc=center(1)%z/real(N_particle)  

  do i=1,N_particle
    rci=0.d0
 
    xi=molecule(i)%x
    yi=molecule(i)%y
    zi=molecule(i)%z
    ri=molecule(i)%radius

    r_2=(xi-xc)**2+(yi-yc)**2+(zi-zc)**2
    rci=sqrt(r_2)+ri
    prot_id(1)%radius=max(rci,prot_id(1)%radius) 

  end do
  write(6,form_tens) 'Protein number/radius', real(1), prot_id(1)%radius

  Npositions=int(4.d0*pi*(prot_id(1)%radius)**2/PtDens)+1
  write(22,*) Npositions
  close(22)  
 
  write(6,*) 'Number or starting positions for ligand: ',Npositions
  close(6)

  stop 'area of receptor done'

end program Get_receptor_area
