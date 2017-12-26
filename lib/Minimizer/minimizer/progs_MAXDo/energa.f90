module energa

  use particles
  use run_parameter
  use microb 
  use lj_red
  use born
  use constrain

  implicit none

contains

subroutine energy(position,etot,elj,elec,grad)
!=============================================

  integer :: i,j,k,Npart,part
  integer :: ic,jc,particle,prot

  real(8), intent(OUT) :: etot,elj,elec

  real(8) ::  r_eq,r_2
  real(8) ::  xc,yc,zc
  real(8) ::  fx,fy,fz
  real(8) ::  Mx,My,Mz
  real(8) ::  alpha,beta
  real(8) ::  dx,dy,dz
  real(8) ::  Econs
  real(8) ::  Etelec

  real(8),dimension(6),intent(IN)  :: position
  real(8),dimension(6),intent(OUT) :: grad

  real(8),dimension(3,N_particle) :: ftelec
  real(8),dimension(3) :: fcons

  etot=0.0d0
  grad=0.0d0
  Econs=0.d0
  fx_lj(:)=0.0d0
  fy_lj(:)=0.0d0
  fz_lj(:)=0.0d0
  ftelec(:,:)=0.0d0
  fcons(:)=0.d0
  Mx=0.0d0
  My=0.0d0
  Mz=0.0d0

  prot=2
  alpha=position(6)*cdr
  beta=position(4)*cdr

  Npart=prot_id(prot)%Pstot_number 

  call rotation(position,prot)

  call LJpot(elj)
  call SPLelec(elec)

  call force_LJ
  call force_splelec(ftelec)
 
  fx_elec(:N_particle)=330.0d0*ftelec(1,:)
  fy_elec(:N_particle)=330.0d0*ftelec(2,:)
  fz_elec(:N_particle)=330.0d0*ftelec(3,:)

  if(constraint) then
    call Constraint_energy(Econs,position)
    call Constraint_forces(fcons,position)

    grad(1)=grad(1)-fcons(1)
    grad(2)=grad(2)-fcons(2)
    grad(3)=grad(3)-fcons(3)
  endif 

  etot=elj+elec+Econs

  do part=1,Npart
   
    i=prot_id(prot)%Pstot_item(part)

    dx=molecule(i)%x*side_x-position(1)
    dy=molecule(i)%y*side_y-position(2)    
    dz=molecule(i)%z*side_z-position(3)

    fx=0.597d0*fx_lj(i)+fx_elec(i)
    fy=0.597d0*fy_lj(i)+fy_elec(i)
    fz=0.597d0*fz_lj(i)+fz_elec(i)

    grad(1)=grad(1)-fx
    grad(2)=grad(2)-fy
    grad(3)=grad(3)-fz

    Mx=Mx+dy*fz-dz*fy
    My=My+dz*fx-dx*fz
    Mz=Mz+dx*fy-dy*fx

  end do
  
  grad(4)=-(cos(alpha)*Mx+sin(alpha)*My)
  grad(5)=-cos(beta)*cos(alpha)*My+cos(beta)*sin(alpha)*Mx-sin(beta)*Mz
  grad(6)=-Mz

  do i=4,6
    grad(i)=grad(i)*cdr    
  end do

  return

end subroutine energy

subroutine move(niter,position,Etot,grad)
!========================================

  integer :: i
  integer, intent(IN) :: niter

  real(8), intent(OUT) :: Etot
  real(8) ::  elj,elec

  real(8),dimension(6),intent(IN) :: position
  real(8),dimension(6),intent(OUT) :: grad

  call energy(position,Etot,elj,elec,grad)
  evalf_number=evalf_number+1

  Eold=Etot

  return

end subroutine move

end module energa
