module timing

  implicit none
  
  real(8),dimension(2) :: tarray
  real(8) ::  start_time,actual_time,restart_time
  real(8), parameter :: restart_block_time=300.
  
  
contains 

subroutine initial_time
!======================

  real(8) ::  dummy_time
  real(8) ::  rtc
  
  dummy_time  =rtc()
  start_time  =dummy_time
  actual_time =dummy_time
  restart_time=dummy_time+restart_block_time
  
  return
  
end subroutine initial_time

real function elapsed_time()
!===========================

  real(8) ::  dummy_time
  real(8) ::  rtc 
  
  dummy_time =rtc()
  actual_time=dummy_time
  
  elapsed_time=actual_time-start_time
  
  return
  
end function elapsed_time

end module timing
