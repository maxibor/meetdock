module springs

  use run_parameter
  use particles
  use format_declaration

  implicit none

  contains

subroutine write_pdb_file(prot,file_name)
!========================================

  integer :: i,position
  integer :: end,start 
  integer :: first
  integer :: Nps,parti,Nca
  
  integer, intent(IN) :: prot

  real(8) ::  xi,yi,zi
  real(8) ::  ri,qi,ai

  character*50, intent(IN) :: file_name
  character*50 pdb_file
  character*1  chain
  character*1  pnu, pnui
  character*4  amino
  character*2  PsA 

  end=index(file_name,' ')-1

  pdb_file='pdb_files/'//protein_name(prot)//'.'//file_name(:end)//'.pdb' 
  open(22,file=pdb_file)

  write(22,form_line) 'HEADER '//pdb_file//' after simulation'

  Nps=prot_id(prot)%Pstot_number
  Nca=prot_id(prot)%Ca_number

  do i=1,Nca

    parti=prot_id(prot)%Ca_item(i)

    xi=molecule(parti)%x*side_x
    yi=molecule(parti)%y*side_y
    zi=molecule(parti)%z*side_z

    ri=molecule(parti)%radius
    qi=molecule(parti)%charge
  
    position=residue(parti)%number

    amino=residue(parti)%aa
    chain=residue(parti)%chain
    PsA=residue(parti)%type
      
    write(22,form_prot) 'ATOM',parti,PsA,amino,chain,position,xi,yi,zi,molecule(parti)%energy,qi,ri

  end do
  
  do i=1,Nps

    parti=prot_id(prot)%Pstot_item(i)

    xi=molecule(parti)%x*side_x
    yi=molecule(parti)%y*side_y
    zi=molecule(parti)%z*side_z

    ri=molecule(parti)%radius
    qi=molecule(parti)%charge
  
    position=residue(parti)%number

    amino=residue(parti)%aa
    chain=residue(parti)%chain
    PsA=residue(parti)%type
  
    if(Psa=='CB') then    
      write(22,form_prot) 'ATOM',parti,PsA,amino,chain,position,xi,yi,zi,molecule(parti)%energy,qi,ri
    end if 
  end do

  do i=1,Nps

    parti=prot_id(prot)%Pstot_item(i)

    xi=molecule(parti)%x*side_x
    yi=molecule(parti)%y*side_y
    zi=molecule(parti)%z*side_z

    ri=molecule(parti)%radius
    qi=molecule(parti)%charge
  
    position=residue(parti)%number

    amino=residue(parti)%aa
    chain=residue(parti)%chain
    PsA=residue(parti)%type
  
    if(Psa=='CG') then    
      write(22,form_prot) 'ATOM',parti,PsA,amino,chain,position,xi,yi,zi,molecule(parti)%energy,qi,ri
    end if 
  end do

  write(22,form_prot) 'TER  ',parti,PsA,amino,chain,position

  close(22)

  return

end subroutine write_pdb_file

end module springs
