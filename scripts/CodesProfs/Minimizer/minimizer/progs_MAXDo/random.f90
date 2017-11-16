module random
implicit none

contains

real function ranval()
!=================================
  real :: dummy
  
  call random_number(dummy)
  if(dummy==0.) then
    call random_seed
    call random_number(dummy)
  end if
  ranval = dble(dummy)
  return
end function ranval

end module random
