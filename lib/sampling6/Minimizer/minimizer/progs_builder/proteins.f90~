module proteins

  use run_parameter
  use particles
  use format_declaration

  implicit none

  contains

subroutine protein_list
!======================

  integer :: i,j,imin,imin1,imin2
  integer :: nunit
  integer :: nsep

  real(8) :: Emin, Emin1,Emin2,Eav,Std
  real(8) :: Edens, score

  character*21 selection_branch
  character*250 line

  N_positions=0
  Eav=0.d0
  Std=0.d0

  do i=1,2
    read(20,*) protein_file(i)
    read(20,*) protein_name(i)

    nunit=30+i
 
    open(unit=nunit,file=protein_file(i),status='old')
 
  end do

  read(20,*) selection_branch  
  selection =decide_branch (selection_branch,'selection            ')

  read(20,*) selpos
  if(selection) write(6,*) 'building selected position', selpos
  

    write(6,*) 'relocating ligand protein'
    i=0
    imin=0
    Emin=0.d0 
    Edens=0.d0
    do
      read(unit=21,fmt=form_line,end=999) line
      if(line(2:8)=='Docking') cycle
      if(line(120:127)=='0.000000') cycle
      i=i+1
       read(line,form_glob) Npos(i),Nrot(i),&
                           (New_position(j,i),j=1,3), New_position(6,i), New_position(4,i), New_position(5,i),&
                            Elj(i),Ecoul(i),Etot(i)
      Emin=min(Emin,Etot(i))

      if(Emin==Etot(i))  then
        imin=Npos(i)
      end if 
    end do

    999 continue  
    N_positions=i
    Eav=sum(Etot)/real(size(Etot))

    do j=1,N_positions
      Std=Std+(Etot(j)-Eav)**2
    end do

    if(N_positions>0) Std=sqrt(Std/real(N_positions)) 
 
  write(6,*) 'Number of valid positions: ', N_positions
  write(6,*) 'Minimum energy for position: ', imin, Emin
  write(6,*) 'Average energy and standard deviation', Eav, Std

  write(6,*) 'Receptor protein ', protein_name(1) 
  write(6,*) 'Ligand protein ', protein_name(2) 

  return

end subroutine protein_list

subroutine get_centers(talk)
!===========================

  logical, intent(IN) :: talk

  integer :: prot, part, i
  integer :: Npart

  real(8) :: x,y,z
  real(8) :: x1,y1,z1
  real(8) :: x2,y2,z2
  real(8) :: dx,dy,dz

  do prot=1,2
   
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

  x1=center(1)%x
  y1=center(1)%y
  z1=center(1)%z

  x2=center(2)%x
  y2=center(2)%y
  z2=center(2)%z

  dx=x2-x1
  dy=y2-y1
  dz=z2-z1

  Prot_sep=sqrt(dx**2+dy**2+dz**2)

  vector%x=dx/Prot_sep
  vector%y=dy/Prot_sep
  vector%z=dz/Prot_sep

  theta=acos(dz/Prot_sep)

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
  real(8) :: r2,rci

  prot_id%radius=0.0

  do prot=1,2

    Npart=prot_id(prot)%number
    
    xc=center(prot)%x
    yc=center(prot)%y
    zc=center(prot)%z

    do parti=1,Npart

      rci=0.0 

      i=prot_id(prot)%item(parti)

      xi=molecule(i)%x       
      yi=molecule(i)%y       
      zi=molecule(i)%z       

      r2=(xi-xc)**2+(yi-yc)**2+(zi-zc)**2 

      rci=2.d0*sqrt(r2)/3.d0

      prot_id(prot)%radius=max(rci,prot_id(prot)%radius) 

    end do
    write(6,form_tens) 'Protein number/radius', real(prot), prot_id(prot)%radius
  end do 
 
  write(6,*) 
 
  return

end subroutine get_prot_radius

end module proteins
