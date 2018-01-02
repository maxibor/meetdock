module timing

  implicit none
  
  real(8) ,dimension(2) :: tarray
  real(8) ::  start_time,actual_time,restart_time
  real(8) , parameter :: restart_block_time=300.
  
  
contains 

subroutine initial_time
!======================

  real(8) ::  dummy_time
  real(8) ::  etime
  
  dummy_time  =etime(tarray)
  start_time  =tarray(1)
  actual_time =tarray(1)
  restart_time=tarray(1)+restart_block_time
  
  return
  
end subroutine initial_time

real(8) function elapsed_time()
!===========================

  real(8) ::  dummy_time
  real(8) ::  etime
  
  dummy_time =etime(tarray)
  actual_time=tarray(1)
  
  elapsed_time=actual_time-start_time
  
  return
  
end function elapsed_time

end module timing
