module particles

  implicit none 

  type molecule_var
    real(8) ::  x,y,z,radius,energy,charge
  end type molecule_var 

  type residue_var
    character*2 type
    character*4 aa
    character*1 chain
    integer :: number, atom, prot
  end type residue_var

  type protlist_var
    integer, dimension(:),pointer :: Pstot_item, Ca_item
    integer :: Pstot_number, Ca_number
    character*1 chain
    real(8) ::  radius
  end type protlist_var

  type average_var
    integer :: number
    real :: sum
  end type average_var

  type (molecule_var) :: vector

  type (average_var) :: av_evalf

  integer :: N_particle, N3, Nvar, Ntot
  integer :: N_protein
  integer :: Nvect1, Nvect2
  integer :: evalf_number
  
  real(8) :: Prot_sep
  real(8) :: theta0, phi0, theta, phi
  real(8) :: alpha0,beta0,gamma0
  real(8) :: Eold
  real(8) :: total_energy,saddle_energy
  real(8) :: eigenvalue

  real(8),dimension(6) :: Start_Lig, Old_Lig, Lig_position, Lig_ref
  real(8),dimension(6) :: initial_direction,projection
  
end module particles
