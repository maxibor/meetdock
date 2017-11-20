module particles

  implicit none 

  type molecule_var
    character*3 type
    character*1 chain
    character*1 icode ! Add by Lydie 20/03/15
    integer :: atom,resid
    real(8) :: x,y,z
  end type molecule_var 

  type residue_var
    character*4 aa
    character*1 chain
    character*1 icode ! Add by Lydie 20/03/15
    integer :: number
    logical :: refint
  end type residue_var

  type protlist_var
    integer, dimension( : ),pointer :: item, Ca_item
    integer :: number, Ca_number
    character*1 chain
    character*1 icode ! Add by Lydie 20/03/15
    real(8) :: radius
  end type protlist_var

  type complex_var
    real :: Intarea,psurf
    real :: npfraction, bufraction
    real :: RP 
  end type complex_var

  type ( molecule_var ), allocatable, dimension( : ) :: molecule
  type ( molecule_var ), allocatable, dimension( : ) :: old_position
  type ( molecule_var ), dimension(2) :: center

  type ( molecule_var ) :: vector

  type ( residue_var ), allocatable, dimension( : ) :: residue

  type ( complex_var ), allocatable, dimension( : ) :: Protcomplex

  type ( protlist_var ), dimension (2) :: prot_id

  integer :: N_particle, N_restot, N_positions
  integer, dimension(2) :: N_residue
  integer, dimension(:), allocatable ::Nrot,Npos,Erank ! added by Lydie (9/02/2015))

  real(8) :: Prot_sep, Emin ! Added by Lydie (9/02/15)
  real(8) :: theta0, phi0, theta, phi
  real(8) :: a0,b0,g0
 
  real(8),dimension(6) :: Start_position, Old_Lig, End_position
  real(8),dimension(:), allocatable :: Elj
  real(8),dimension(:), allocatable :: Ecoul
  real(8),dimension(:), allocatable :: Etot
  real(8),dimension(:), allocatable :: Recrate,Ligrate
  real(8), dimension(:,:), allocatable :: New_position

  character*6, dimension(2) :: protein_name
  
  logical, dimension(:,:), allocatable :: interres 

end module particles
