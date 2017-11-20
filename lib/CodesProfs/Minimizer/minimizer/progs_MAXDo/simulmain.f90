program Global_search_for_docking

use run_parameter
use particles
use timing
use proteins
use springs
use zacharias
use mapping 

  implicit none
  
  real(8) ::  E1, E2, E3, Et

  integer :: i
  integer :: loop_start=1
  
  character*50 :: sname

  sname='start'

  call initial_time
  call in_put
    
  do i=1,N_prot_max
    prot_id(i)%Pstot_number=0   
    prot_id(i)%Ca_number=0   
    allocate(prot_id(i)%Pstot_item(N_part_max))
    allocate(prot_id(i)%Ca_item(N_part_max))  
  end do  

  call protein_list
  call make_model
  call get_centers(.false.)
  call get_prot_radius
  call get_centers(.true.)
!  do i=1,N_protein
!    call write_pdb_file(i,sname)
!  end do
 
  start_position(:)=molecule(:)

  write(6,form_text)'making potential map'
  call make_potential_map
  stop 'mapping done' 

  stop 'all done'

end program Global_search_for_docking
