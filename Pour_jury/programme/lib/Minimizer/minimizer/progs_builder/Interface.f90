Program PDBbuilder

  use run_parameter
  use particles
  use springs
  use format_declaration
  use proteins
  use microb

  implicit none

  integer :: i,j
  integer :: pos

  call in_put

  allocate(molecule(N_part_max))
  allocate(old_position(N_part_max))
  allocate(residue(N_part_max))
  allocate(Nrot(N_posi_max))
  allocate(Npos(N_posi_max))
  allocate(Recrate(N_posi_max))
  allocate(Ligrate(N_posi_max))
  allocate(Elj(N_posi_max))
  allocate(Ecoul(N_posi_max))
  allocate(Etot(N_posi_max))
  allocate(Protcomplex(N_posi_max))
  allocate(New_position(6,N_posi_max))
  do i=1,2
    allocate(prot_id(i)%item(N_part_max))
    allocate(prot_id(i)%Ca_item(N_part_max))
  end do
  allocate(interres(N_res_max,N_posi_max))

  call protein_list
!  stop 'list done'
  call read_pdb_file
  call get_centers(.true.)
  call start_rotation(Start_position)
  if(selection) then
    do pos=1,N_positions
      if(Npos(pos)==selpos) then 
        write(6,*) 'relocating position: ',Npos(pos)
        call rotation(New_position(:,pos),2,.false.)
        call write_pdb_file(Npos(pos))
        call get_centers(.true.)
        call start_rotation(End_position)
      end if
    end do
    else
    do pos=1,N_positions
        write(6,*) 'relocating position: ',pos
        call rotation(New_position(:,pos),2,.false.)
        call write_pdb_file(pos)
    end do
  end if 


  stop 'Interface done' 
 
end program PDBbuilder
