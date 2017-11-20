module constrain
 
  use particles
  use run_parameter

  implicit none

  contains

subroutine Constraint_energy(Econs,position)
!===========================================

  integer :: i

  real(8), intent(OUT) :: Econs  
  real(8), dimension(6), intent(IN) :: position

  real(8) ::  x1,y1,z1
  real(8) ::  x2,y2,z2
  real(8) ::  dx,dy,dz
  real(8) ::  dist2

  real(8), dimension(3) :: Rlig, R0

  x1=center(1)%x*side_x
  y1=center(1)%y*side_y
  z1=center(1)%z*side_z

  R0(1)=sin(theta0)*cos(phi0)
  R0(2)=sin(theta0)*sin(phi0)
  R0(3)=cos(theta0)

  Rlig(1)=position(1)-x1
  Rlig(2)=position(2)-y1
  Rlig(3)=position(3)-z1

  dist2=dot_product(Rlig,Rlig)-dot_product(Rlig,R0)**2

  Econs=gcons*dist2 

  return

end subroutine Constraint_energy

subroutine Constraint_forces(fcons,position)
!===========================================
  
  real(8), dimension(3), intent(OUT) :: fcons
  real(8), dimension(6), intent(IN) :: position

  real(8) ::   x1,y1,z1
  real(8) ::   dist2

  real(8), dimension(3) :: Rlig, R0

  x1=center(1)%x*side_x
  y1=center(1)%y*side_y
  z1=center(1)%z*side_z

  R0(1)=sin(theta0)*cos(phi0)
  R0(2)=sin(theta0)*sin(phi0)
  R0(3)=cos(theta0)

  Rlig(1)=position(1)-x1
  Rlig(2)=position(2)-y1
  Rlig(3)=position(3)-z1
  
  fcons=-2.0*gcons*(Rlig-dot_product(Rlig,R0)*R0)
  
  return

end subroutine Constraint_forces

end module constrain

