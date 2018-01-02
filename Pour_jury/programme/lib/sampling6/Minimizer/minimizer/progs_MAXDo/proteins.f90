module proteins

  use run_parameter
  use particles
  use format_declaration

  implicit none

  contains

subroutine protein_list
!======================

  integer :: i

  N_protein=0
  i=0

  do
    read(20,*,end=999) protein_file(i+1)
    read(20,*,end=999) protein_name(i+1)

    i=i+1
  end do

  999 continue

  N_protein=i

  write(6,form_tens) 'Number of proteins  :', real(N_protein)
  write(6,form_c2) (protein_name(i), i=1,N_protein) 

  return

end subroutine protein_list

subroutine get_centers(talk)
!===========================

  logical, intent(IN) :: talk

  integer :: prot, part, i
  integer :: Npart

  real(8) ::  x,y,z
  real(8) ::  x1,y1,z1
  real(8) ::  x2,y2,z2
  real(8) ::  dx,dy,dz

  do prot=1,N_protein
   
    x=0.0
    y=0.0
    z=0.0

    Npart=prot_id(prot)%Ca_number

    do part=1,Npart
      i=prot_id(prot)%Ca_item(part) 

      x=x+molecule(i)%x
      y=y+molecule(i)%y
      z=z+molecule(i)%z
    end do

    center(prot)%x=x/real(Npart)
    center(prot)%y=y/real(Npart)
    center(prot)%z=z/real(Npart)

  end do

  x1=center(1)%x*side_x 
  y1=center(1)%y*side_y 
  z1=center(1)%z*side_z 

  x2=center(2)%x*side_x 
  y2=center(2)%y*side_y 
  z2=center(2)%z*side_z 

  dx=x2-x1
  dy=y2-y1
  dz=z2-z1

  Prot_sep=sqrt(dx**2+dy**2+dz**2)

  vector%x=dx/Prot_sep
  vector%y=dy/Prot_sep
  vector%z=dz/Prot_sep

  if(Prot_sep==0.d0) then
    theta=0.d0
  else
    theta=acos(dz/Prot_sep)
  end if

  if(abs(dz)==Prot_sep) then
    phi=0.d0
  else
    if(dy>=0.d0) then
      phi=acos(dx/sqrt(dx**2+dy**2))
    else
      phi=2.0*pi-acos(dx/sqrt(dx**2+dy**2))
    end if
  end if   

  theta0=theta
  phi0=phi

  if(talk) then
    write(6,form_tens) 'Receptor position', x1,y1,z1
    write(6,form_tens) 'ligand position  ', x2,y2,z2
    write(6,form_tens) 'ligand-receptor separation ', Prot_sep
    write(6,form_tens) 'ligand-receptor orientation theta/phi', theta,phi
    write(6,  *  )
  end if

  return  

end subroutine get_centers

subroutine get_prot_radius
!=========================

  integer :: parti,prot, i
  integer :: Npart
 
  real(8) :: xc,yc,zc
  real(8) :: xi,yi,zi
  real(8) :: dx,dy,dz
  real(8) :: ri, r2,rci

  prot_id(:)%radius=0.0

  do prot=1,N_protein

    Npart=prot_id(prot)%Pstot_number
    
    xc=center(prot)%x
    yc=center(prot)%y
    zc=center(prot)%z

    do parti=1,Npart

      rci=0.d0 

      i=prot_id(prot)%Pstot_item(parti)

      xi=molecule(i)%x       
      yi=molecule(i)%y       
      zi=molecule(i)%z       

      ri=molecule(i)%radius

      r2=(xi-xc)**2+(yi-yc)**2+(zi-zc)**2 

      rci=sqrt(r2)+ri
!      rci=2.d0*sqrt(r2)/3.d0

      prot_id(prot)%radius=max(rci,prot_id(prot)%radius) 

    end do
    write(6,form_tens) 'Protein number/radius', real(prot), prot_id(prot)%radius
  end do 
 
  write(6,*) 
 
!  if(protein_file(1)==protein_file(2)) then
  if(Prot_sep==0.d0) then
    Npart=prot_id(2)%Pstot_number
    do i=1,Npart
      parti=prot_id(2)%Pstot_item(i)

      molecule(parti)%x=molecule(parti)%x+2.d0
      molecule(parti)%y=molecule(parti)%y+2.d0
      molecule(parti)%z=molecule(parti)%z+2.d0
    end do
    old_position(:)=molecule(:)
    write(6,*) 'Moving superposed ligand'
  end if

  return

end subroutine get_prot_radius

end module proteins
