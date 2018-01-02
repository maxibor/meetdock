module compute_distance

use run_parameter

  implicit none

contains

subroutine distance(x1,y1,z1,x2,y2,z2,dx,dy,dz,r_2)
!==================================================
  real(8) ::  x1,y1,z1,x2,y2,z2,dx,dy,dz
  real(8) ::  r_2
  
  dx=x1-x2
  dy=y1-y2
  dz=z1-z2
  
  dx=dx*side_x
  dy=dy*side_y
  dz=dz*side_z
  
  r_2=dx*dx+dy*dy+dz*dz

  return
  
end subroutine distance


end module compute_distance
