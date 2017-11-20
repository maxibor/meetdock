module microb

  use particles
  use run_parameter
    
  implicit none

contains

subroutine start_rotation(position)
!==================================

  integer :: prot,part1,part2

  real(8) ::  xc,yc,zc
  real(8) ::  x1,y1,z1
  real(8) ::  x2,y2,z2
  real(8) ::  xi2,yi2,zi2
  real(8) ::  xii2,yii2,zii2
  real(8) ::  p1,r1, p2
  real(8) ::  alpha,beta,gamma
  real(8) ::  c_a,s_a,c_b,s_b, c_g,s_g

  real(8),dimension(6), intent(OUT) :: position

  prot=2   

  xc=center(prot)%x
  yc=center(prot)%y
  zc=center(prot)%z

  part1=prot_id(prot)%Ca_item(1)
  part2=prot_id(prot)%Ca_item(5)

  x1=molecule(part1)%x-xc
  y1=molecule(part1)%y-yc
  z1=molecule(part1)%z-zc

  x2=molecule(part2)%x-xc
  y2=molecule(part2)%y-yc
  z2=molecule(part2)%z-zc

  p1=sqrt(x1**2+y1**2)
  r1=sqrt(x1**2+y1**2+z1**2)  

  c_a= y1/p1
  s_a=-x1/p1

  c_b=p1/r1
  s_b=z1/r1

  alpha=acos(c_a)*crd
  if(s_a<0.0) alpha=-alpha
  alpha0=alpha


  beta=acos(c_b)*crd
  if(s_b<0.0) beta=-beta
  beta0=beta

  xi2=x2*c_a-y2*s_a
  yi2=y2*c_a+x2*s_a
  zi2=z2

  xii2=xi2
  yii2=yi2*c_b+zi2*s_b
  zii2=zi2*c_b-yi2*s_b

  p2=sqrt(zii2**2+xii2**2)
 
  c_g=zii2/p2
  s_g=xii2/p2
  
  gamma=acos(c_g)*crd
  if(s_g<0.d0) gamma=-gamma
  gamma0=gamma

  position(1)=xc*side_x
  position(2)=yc*side_y
  position(3)=zc*side_z
  position(6)=alpha
  position(4)=beta
  position(5)=gamma  

  write(6,form_tens) 'starting angles alpha/beta/gamma:', alpha, beta, gamma

  return

end subroutine start_rotation

subroutine rotation(position,prot)
!=================================

  integer :: Npart, part, i

  integer, intent(IN) :: prot

  real(8) ::  xi,yi,zi
  real(8) ::  x1i,y1i,z1i
  real(8) ::  x2i,y2i,z2i
  real(8) ::  x3i,y3i,z3i
  real(8) ::  rx,ry,rz
  real(8) ::  dx,dy,dz,da,db,dg
  real(8) ::  a,b,g
  real(8) ::  c_a,c_b,c_g
  real(8) ::  c_a0,c_b0
  real(8) ::  s_a,s_b,s_g
  real(8) ::  s_a0,s_b0
  
  real(8),dimension(6),intent(IN) :: position
  real(8),dimension(6) :: dlig

  Npart=prot_id(prot)%Pstot_number

  dlig(:)=position(:)-Old_Lig(:)

  a=dlig(6)
  b=dlig(4)
  g=dlig(5)

  if(maxval(abs(dlig))==0.0d0) then
    write(6,*) 'No rotation here'
    go to 100
  end if
 
  c_a=cos(a*cdr)
  s_a=sin(a*cdr)
  c_b=cos(b*cdr)
  s_b=sin(b*cdr)
  c_g=cos(g*cdr)
  s_g=sin(g*cdr)
  
  c_a0=cos(position(6)*cdr)
  s_a0=sin(position(6)*cdr)
  c_b0=cos(position(4)*cdr)
  s_b0=sin(position(4)*cdr)

  do i=1,Npart

    part=prot_id(prot)%Pstot_item(i)

    xi=old_position(part)%x-Old_Lig(1)/side_x
    yi=old_position(part)%y-Old_Lig(2)/side_y
    zi=old_position(part)%z-Old_Lig(3)/side_z

! rotation de dalpha
    x1i=c_a*xi-s_a*yi
    y1i=c_a*yi+s_a*xi
    z1i=zi

! rotation de dbeta
    x2i=(c_a0*c_a0+(1.0-c_a0*c_a0)*c_b)*x1i+c_a0*s_a0*(1.0-c_b)*y1i+s_a0*s_b*z1i
    y2i=c_a0*s_a0*(1.0-c_b)*x1i+(s_a0*s_a0+(1.0-s_a0*s_a0)*c_b)*y1i-c_a0*s_b*z1i
    z2i=-s_a0*s_b*x1i+c_a0*s_b*y1i+c_b*z1i

    rx=-s_a0*c_b0
    ry= c_a0*c_b0
    rz= s_b0 

! rotation de dgamma 
    x3i=(rx*rx+(1.0-rx*rx)*c_g)*x2i+(rx*ry*(1.0-c_g)-rz*s_g)*y2i+(rx*rz*(1.0-c_g)+ry*s_g)*z2i
    y3i=(rx*ry*(1.0-c_g)+rz*s_g)*x2i+(ry*ry+(1.0-ry*ry)*c_g)*y2i+(ry*rz*(1.0-c_g)-rx*s_g)*z2i
    z3i=(rx*rz*(1.0-c_g)-ry*s_g)*x2i+(ry*rz*(1.0-c_g)+rx*s_g)*y2i+(rz*rz+(1.0-rz*rz)*c_g)*z2i
 
    molecule(part)%x=position(1)/side_x+x3i
    molecule(part)%y=position(2)/side_y+y3i
    molecule(part)%z=position(3)/side_z+z3i

  end do

100  continue 

  return

end subroutine rotation
  
end module microb
