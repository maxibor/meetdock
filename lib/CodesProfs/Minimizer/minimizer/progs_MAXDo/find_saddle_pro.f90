!  Subroutine find_saddle
!
!  This subroutine initiates the random displacement at the start
!  of the ART algorithm. 
!
!  After random escape direction has been selected, the routine call 
!  saddle_converge which will try to bring the configuration to a saddle point.
!
!  If the convergence fails, find_saddle will restart; if it succeeds, it saves 
!  the event and returns to the main loop.
!
!  The displacement can be either LOCAL and involve a single atom
!  and its neareast neighbours or
!
!  NON-LOCAL and involve ALL the atoms.
!
!  For large cells, it is preferable to use a local initial
!  displacement to prevent the creation of many trajectories
!  at the same time in different sections of the cell.
!
!   Normand Mousseau  19 June 2001
!
module find_saddle_pro

  use saddle_converge_pro  
  use run_parameter
  use random

  implicit none

contains  
 
subroutine find_saddle(success)
!==============================

  logical, intent(out) :: success
  integer :: ret
  real(8) :: fperp, fpar, saddle_energy
  real(8) :: mean_evalf

  evalf_number = 0
  
! And copy the reference position into the working vector
  Lig_position = Lig_ref  

! These two subroutines (local_move() and global_move()) modify the vector pos and 
! generate a vector of length 1 indicating the direction of the random displacement
  call global_move()

! Now, activate per atom
  call saddle_converge(ret,saddle_energy,fpar,fperp)

  av_evalf%number=av_evalf%number+1
  av_evalf%sum=av_evalf%sum+real(evalf_number) 

  if((ret>0).and.((ret<30000))) then 
! We write out various information to both screen and file
     mean_evalf=av_evalf%sum/real(av_evalf%number)     
     write(6,"(' ','Total energy S: ',f10.4,' fpar: ',f12.6,' fperp: ',f12.6,&
               ' ret: ',i6,' force eval,mean: ',i6,f12.3)")&
           saddle_energy, fpar, fperp, ret, evalf_number, mean_evalf

  endif

! If the activation did not converge, for whatever reason, we restart the 
! routine and do not accept the new position
  if ( ( ret <= 0) .or. ( (ret > 30000) )  ) then
    success = .false.
  else
    success = .true.
  endif

  return

end subroutine find_saddle

subroutine global_move()
!=======================

  integer :: i
  real(8) :: norm,dummy
  real(8), dimension(Nvar) :: delpos
  real(8), dimension(6) :: scal 
 
  scal(1:3)=1.d0
  scal(4:6)=15.d0 

  dummy=ranval()

! Generate a random displacement
  do i=1,Nvar
    delpos(i)=0.5d0-ranval()
  end do

! Keep the center of mass fixed 
!  call center2(delpos)
  
! And renormalize the total displacement to the value desired
  norm = 0.d0
  norm=dot_product(delpos,delpos) 

!  This renormalizes in angstroems to a displacement INITSTEPSIZE
  norm = INITSTEPSIZE / sqrt(norm)
  delpos = delpos * norm

! Update the position using this random displacement
  Lig_position = Lig_position +  delpos*scal  ! Vectorial operation

! Now, we normalize delpos to get the initial_direction 

  initial_direction = delpos    ! Vectorial operation
  norm = 0.d0
  norm=dot_product(initial_direction,initial_direction)
  norm = 1.d0 / sqrt (norm)
  initial_direction  = initial_direction * norm

  return

end subroutine global_move

end module find_saddle_pro
