module springs

  use run_parameter
  use particles
  use format_declaration

  implicit none

  contains

subroutine read_pdb_file
!=======================

  integer :: i,itot,prot,nunit
  integer :: res,restot
  integer :: Nca
  character*80 line

  N_particle=0
  N_restot=0
  itot=0
  restot=0 

  do prot=1,2

    write(6,*) 'reading pdb', prot

    nunit=30+prot
    i=0
    res=0
    Nca=0

    do
      open(unit=nunit,file=protein_file(prot),status='old')
      read(unit=nunit,fmt=form_line,end=999) line

      if(line(:4)=='ATOM') then
        i=i+1
        itot=itot+1
        if(itot>N_part_max) stop 'too many atoms'

        ! WARNING add res==0 if the protein do not begin by the N atom !!!
        ! correction le 11/07/2013
        if(line(14:15)=='N '.or. res==0) then
          res=res+1
          restot=restot+1
          ! Modification by Lydie 20/03/15
          read(line,form_pdb) molecule(itot)%atom, molecule(itot)%type, residue(restot)%aa, residue(restot)%chain,&
                              residue(restot)%number,residue(restot)%icode, molecule(itot)%x, molecule(itot)%y, molecule(itot)%z

          molecule(itot)%resid=residue(restot)%number
          molecule(itot)%chain=residue(restot)%chain
          molecule(itot)%icode=residue(restot)%icode ! Add by Lydie 20/03/15
          if(res==1) then
            prot_id(prot)%chain=residue(restot)%chain
            prot_id(prot)%icode=residue(restot)%icode ! Add by Lydie 20/03/15
          end if
          
          if(line(14:15)=='CA') then
            Nca=Nca+1
            prot_id(prot)%Ca_item(res)=itot
          end if
        else
          read(line,form_ato) molecule(itot)%atom, molecule(itot)%type, molecule(itot)%resid,&
                              molecule(itot)%x, molecule(itot)%y, molecule(itot)%z
          molecule(itot)%resid=residue(restot)%number

          if(line(14:15)=='CA') then
            Nca=Nca+1
            prot_id(prot)%Ca_item(res)=itot
          end if
        end if
 
        prot_id(prot)%item(i)=itot
      end if
    end do

    999 continue
 
    prot_id(prot)%number=i
    prot_id(prot)%Ca_number=Nca 
    N_residue(prot)=res 
    write(6,*) 'atoms in protein ',prot,': ',i
    write(6,*) 'residues in protein ',prot,': ',res, 'Ca', Nca
    close(nunit) ! modif by Lydie 6/02/15
  end do
  
  old_position(:)=molecule(:)

  N_particle=itot
  N_restot=restot
  write(6,*) 'Number of atoms :', N_particle
  write(6,*) 'Number of residues :', N_restot

  return

end subroutine read_pdb_file

subroutine write_pdb_file(dockpos)
!=================================

  integer, intent(IN) :: dockpos 

  integer :: i,j,position,parti
  integer :: end,start,resi 
  integer :: first
  integer :: Np2,place

  real(8) :: xi,yi,zi

  character*80 pdb_file
  character*5  nu
  character*1  pnu, pnui
  character*1  chain
  character*1  icode ! Add by Lydie 20/03/15
  character*3  typi
  character*4  aai

  write(nu,'(i5)') dockpos

  if(dockpos<10) then
    first=index(nu,' ')+4
  else if(dockpos<100) then
    first=index(nu,' ')+3
  else if(dockpos<1000) then
    first=index(nu,' ')+2
  else if(dockpos<10000) then
    first=index(nu,' ')+1
  else
    first=1
  end if  

  pdb_file='pdb_files/'//protein_name(1)//'-'//protein_name(2)//'.min'//nu(first:5)//'.pdb'

  open(22,file=pdb_file)

  write(22,form_line) 'HEADER '//pdb_file//' position '//nu(first:5)//''

  Np2=prot_id(2)%number
  chain=prot_id(2)%chain
  icode=prot_id(2)%icode ! Add by Lydie 20/03/15

  do parti=1,Np2

      i=prot_id(2)%item(parti) 

      xi=molecule(i)%x
      yi=molecule(i)%y
      zi=molecule(i)%z

      position=molecule(i)%resid
      do j=N_residue(1)+1,N_restot
        ! Modification by Lydie 20/03/15
        if(residue(j)%number==position.and.residue(j)%chain==molecule(i)%chain.and.residue(j)%icode==molecule(i)%icode) resi=j
      end do
      place=molecule(i)%atom
 
      typi=molecule(i)%type

        ! Modification by Lydie 20/03/15
        write(22,form_prot) 'ATOM',molecule(i)%atom,molecule(i)%type,residue(resi)%aa,residue(resi)%chain,&
                            position,residue(resi)%icode,xi,yi,zi

      if(parti==Np2) then
        write(22,form_chain) 'TER',molecule(i)%atom,residue(resi)%aa,residue(resi)%chain,position
      end if     

  end do

  close(22)
  
  return

end subroutine write_pdb_file

end module springs
