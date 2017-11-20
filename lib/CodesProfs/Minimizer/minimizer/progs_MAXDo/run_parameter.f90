module run_parameter

  use particles
  use format_declaration
  
  implicit none
  
  integer,parameter :: N_part_max=10000
  integer,parameter :: N_prot_max=2
  integer,parameter :: n7=10
  integer,parameter :: maxiter=2000
  integer,parameter :: N_vect_max=10000

  real(8), parameter ::  pi=3.141592654d0
  real(8), parameter :: cdr=0.017453293d0
  real(8), parameter :: crd=57.29577951d0
  
  integer :: nk1,nk2,ngamma
  integer :: nsep1,nsep2,nrot1,nrot2
  integer :: NUMBER_EVENTS

  real(8) ::  temp,temp_pot
  real(8) ::  gcons, lambda
  real(8) ::  gtol,stpfac
  real(8) ::  side_x, side_y, side_z
  real(8) ::  sigmacut
  real(8) ::  sample_dist
  
  logical :: constraint
  logical :: art
  logical :: first_time=.true.
  
  character*21 :: constraint_branch
  character*21 :: art_branch
  
  character*40 :: input_file,output_file
  
  character*80,dimension(N_prot_max) :: protein_file
  character*6, dimension(N_prot_max) :: protein_name 

  type (molecule_var), dimension(N_part_max) :: molecule 
  type (molecule_var), dimension(N_part_max) :: old_position
  type (molecule_var), dimension(N_part_max) :: start_position
  type (molecule_var), dimension(N_part_max) :: center

  integer,dimension(N_vect_max) :: vecposition
  type (molecule_var), dimension(N_vect_max) :: vect_u1
  type (molecule_var), dimension(N_vect_max) :: vect_u2

  type (residue_var), dimension(N_part_max) :: residue

  type (protlist_var), dimension (N_prot_max) :: prot_id

  real(8),dimension(N_vect_max) :: phi1,phi2
  real(8),dimension(N_vect_max) :: theta1,theta2
  real(8),dimension(N_vect_max) :: Psep

  real(8), dimension(N_part_max) :: fx_lj
  real(8), dimension(N_part_max) :: fy_lj
  real(8), dimension(N_part_max) :: fz_lj

  real(8), dimension(N_part_max) :: fx_elec
  real(8), dimension(N_part_max) :: fy_elec
  real(8), dimension(N_part_max) :: fz_elec

! Parametres pour la subroutine saddle_converge  
  integer, parameter :: MAXITERART = 300
  integer, parameter :: MAXIPERP = 1 ! 2
  real(8), parameter :: INCREMENT = 0.020  ! In angstroems 
  real(8), parameter :: FTHRESHOLD = 0.5d0   ! 1.0
  real(8), parameter :: EIGEN_THRESH = -5.0d0 ! -1.0
  real(8), parameter :: FTHRESH2  = FTHRESHOLD * FTHRESHOLD 
  real(8), parameter :: EXITTHRESH = 0.80 ! 1.0

!Parametres pour la subroutine find_saddle
  real(8), parameter :: INITSTEPSIZE = 0.001     !Size of initial displacement in Ang. 
  real(8), parameter :: FRACTIONFRAGMENT = 0.6d0 ! 20% du fragment est déplacé aléatoirement
  integer                     :: natom_displaced   ! Number of local atoms displaced
  real(8), dimension(9)       :: ener
  real(8)                     :: ehigh           

!Parametres pout la subroutine art_protein
!  integer, parameter :: NUMBER_EVENTS = 500    ! Total number of events in this run

  contains 

subroutine in_put
!================

  character (10) :: dummy_1,dummy_2,dummy_3
  
  integer, dimension(8) :: h
  
  call date_and_time(dummy_1,dummy_2,dummy_3,h)
  
  open(99,file='runfile')
  open(98,file='energy.dat') 
  open(97,file='position.dat')
  open(96,file='global.dat') 
 
  read(99,*) input_file
  read(99,*) output_file
  
  open( 5,file=input_file)
  open( 6,file=output_file)
  open( 20,file='proteins.dat',status='old')

  write(6,form_date) '*** Start Simulation on',h(2),'/',h(3),'/',h(1),' at ',h(5),':',h(6),':',h(7),' hours ***'
  write(6,    *    )
  
  read (5,  *   ) gcons,lambda
  write(6,form_r) gcons,lambda
  read (5,  *   ) gtol,stpfac
  write(6,form_r) gtol,stpfac
  read (5,  *   ) temp,temp_pot
  write(6,form_r) temp,temp_pot
  read (5,  *   ) side_x,side_y,side_z
  write(6,form_r) side_x,side_y,side_z
  read (5,  *   ) sigmacut
  write(6,form_r) sigmacut
  read (5,  *   ) sample_dist
  write(6,form_r) sample_dist
  read (5,  *   ) nk1,nk2,ngamma
  write(6,form_i) nk1,nk2,ngamma  
    
  write(6,  *    )
  write(6,form_c1) '********** Activated/deactivated branches **********'
  
  read (5,  *    ) constraint_branch
  write(6,form_c2) constraint_branch 
  read (5,  *    ) art_branch
  write(6,form_c2) art_branch 
  
  write(6,form_c1) '****************************************************'
  write(6,  *    )

  read (5,  *   ) nsep1
  write(6,form_i) nsep1
  read (5,  *   ) nsep2
  write(6,form_i) nsep2
  read (5,  *   ) nrot1
  write(6,form_i) nrot1
  read (5,  *   ) nrot2
  write(6,form_i) nrot2
  read (5,  *   ) NUMBER_EVENTS
  write(6,form_i) NUMBER_EVENTS
  read (5,  *   ) Nvect1
  write(6,form_i) Nvect1
  
  write(6,    *    ) '********************* Files  connected ********************'
  write(6,form_file) 'Input   from file   : ',input_file
  write(6,form_file) 'Output  to   file   : ',output_file
  write(6,    *    ) '***********************************************************'
  write(6,    *    )
  
  constraint=              decide_branch(constraint_branch,'constraint           ')
  art       =                     decide_branch(art_branch,'art                  ')

  fx_elec(:)=0.0
  fy_elec(:)=0.0
  fz_elec(:)=0.0

  av_evalf%number=0
  av_evalf%sum=0.d0

  close(5)
 
  return

end subroutine in_put

subroutine save_data(newsep)
!===========================

  integer, intent(IN) :: newsep

  integer:: nsep,nrot
  real(8) :: Psmin,tmin,pmin
  real(8) :: amin,bmin,gmin
  real(8) :: Erlj,Erelec,Ermin

  character*150 :: line

  open(5,file='input.dat')

  write(5,form_r) gcons,lambda
  write(5,form_r) gtol,stpfac
  write(5,form_r) temp,temp_pot
  write(5,form_r) side_x,side_y,side_z
  write(5,form_r) sigmacut
  write(5,form_r) sample_dist
  write(5,form_i) nk1,nk2,ngamma  
  write(5,form_c2) constraint_branch 
  write(5,form_c2) art_branch 
  write(5,form_i) newsep
  write(5,form_i) nsep2
  write(5,form_i) nrot1
  write(5,form_i) nrot2
  write(5,form_i) NUMBER_EVENTS
  write(5,form_i) Nvect1
  
  close(5)

  open(95,file='temp_global.dat')

  do 
    read(95,fmt=form_dec,end=999) nsep,nrot,Psmin,tmin,pmin,amin,bmin,gmin,Erlj,Erelec,Ermin 
    write(96,form_dec) nsep,nrot,Psmin,tmin,pmin,amin,bmin,gmin,Erlj,Erelec,Ermin
  end do

  999 continue

  close(95)

  return

end subroutine save_data

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
