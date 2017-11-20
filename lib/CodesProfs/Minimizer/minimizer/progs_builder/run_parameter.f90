module run_parameter

  use format_declaration

  implicit none

  integer,parameter :: N_part_max=200000
  integer,parameter :: N_res_max=2000
  integer,parameter :: N_posi_max=10000
  integer,parameter :: r_contact=5.0

  real(8), parameter :: pi=3.141592654d0
  real(8), parameter :: cdr=0.017453293d0
  real(8), parameter :: crd=57.29577951d0

  character*80, dimension(2) ::protein_file

  logical :: selection

  integer :: selpos 

  contains

subroutine in_put
!================

  integer :: i

  open(6,file='output.dat')
  open(20,file='proteins.dat',status='old')
  open(21,file='global.dat',status='old')

  return

end subroutine in_put

logical function decide_branch(which_branch,string)
!==================================================

  character*21 :: which_branch,string
  
  if(which_branch==string) then
    decide_branch=.true.
  else
    decide_branch=.false.
  end if
  
  return
  
end function decide_branch

end module run_parameter
