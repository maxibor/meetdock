module korobov
  
  use run_parameter
  use particles
  use compute_distance
  use random

  implicit none

contains

subroutine kor_vect(nko,vect_u,N_vect,phi,theta)
!===============================================

  integer :: iqa,iqb,iqc
  integer :: i,j,jj,k

  integer, intent(INOUT) :: nko
  integer, intent(OUT) :: N_vect  

  real(8) ::  xb,yb
  real(8) ::  ph,ct,st
  real(8) ::  x1,y1,z1
  real(8) ::  x2,y2,z2
  real(8) ::  dx,dy,dz,r2,r

  real(8),dimension(N_vect_max),intent(OUT) :: phi,theta

  type (molecule_var),dimension(N_vect_max),intent(OUT) :: vect_u

  if(nko>17) nko=17

  iqa=0
  iqb=1
  iqc=0

  jj=0

  do i=1,nko
    iqc=iqa+iqb
    iqa=iqb
    iqb=iqc
  end do
 
  N_vect=iqb

  phi(:)=0.0
  theta(:)=0.0
  vect_u(:)%x=0.0
  vect_u(:)%y=0.0
  vect_u(:)%z=0.0

  do i=1,iqb

    xb=real(i)/real(iqb)
    
    jj=jj+iqa
    if(jj>iqb) jj=jj-iqb
 
    yb=real(jj)/real(iqb)

    ph=2.0*pi*yb 
    phi(i)=ph

    ct=1.0-2*xb
    st=sqrt(1.0-ct*ct)
    theta(i)=acos(ct)

    vect_u(i)%x=st*cos(ph)    
    vect_u(i)%y=st*sin(ph)
    vect_u(i)%z=ct 

  end do

  return

end subroutine kor_vect

subroutine make_vect(vect_u,N_vect,phi,theta)
!============================================

  integer :: vtot
  integer :: ninf
  integer :: i,j,k

  integer, intent(IN) :: N_vect  

  real(8) ::  x,y,z
  real(8) ::  r2,r,p

  real(8),dimension(N_vect_max),intent(OUT) :: phi,theta

  type (molecule_var),dimension(N_vect_max),intent(OUT) :: vect_u


  phi(:)=0.d0
  theta(:)=0.d0
  vect_u(:)%x=0.d0
  vect_u(:)%y=0.d0
  vect_u(:)%z=0.d0

  vtot=0

  do while(vtot<N_vect)
    x=2.d0*ranval()-1.d0
    y=2.d0*ranval()-1.d0
    z=2.d0*ranval()-1.d0

    r2=x**2+y**2+z**2
    if(r2<=1.0.and.r2>0.0) then
      vtot=vtot+1
      r=sqrt(r2)
      p=sqrt(x**2+y**2)

      theta(vtot)=acos(z/r)
      if(p==0.d0) then
        phi(vtot)=0.d0
      else 
        phi(vtot)=acos(x/p)
        if(y<0.d0) phi(vtot)=-phi(vtot)
      end if

      vect_u(vtot)%x=sin(theta(vtot))*cos(phi(vtot)) 
      vect_u(vtot)%y=sin(theta(vtot))*sin(phi(vtot))
      vect_u(vtot)%z=cos(theta(vtot)) 

    end if
  end do

!  write(6,*) minval(theta(1:N_vect))

  do i=1,N_vect
    ninf=0
    do j=1,N_vect
      if(theta(j)<=theta(i)) ninf=ninf+1
    end do
    if(ninf>N_vect) stop 'to many vectors'
    vecposition(ninf)=i
  end do

  open(35,file='angles.dat')
  do i=1,N_vect
    write(35,form_r) real(i),theta(vecposition(i)),phi(vecposition(i))
  end do 
  close(35)

  return

end subroutine make_vect

subroutine get_Psep(vect_u)
!==========================

  integer :: i,j,k, partj, partk
  integer :: Np1, Np2

  real(8) ::  x1,y1,z1
  real(8) ::  x2,y2,z2
  real(8) ::  dx,dy,dz
  real(8) ::  r,r2
  real(8) ::  rmin

  type (molecule_var),dimension(Nvect1),intent(IN) :: vect_u

  Np1=prot_id(1)%Pstot_number
  Np2=prot_id(2)%Pstot_number

  if(Prot_sep==0.d0) then
    Psep(:)=2.d0
  else
    Psep(:)=Prot_sep
  end if

  do i=1,Nvect1
    rmin=200.d0
    do partj=1,Np1         
      j=prot_id(1)%Pstot_item(partj)

      x1=molecule(j)%x
      y1=molecule(j)%y
      z1=molecule(j)%z


      do partk=1,Np2
        k=prot_id(2)%Pstot_item(partk)

        x2=molecule(k)%x+Psep(i)*vect_u1(i)%x-Prot_sep*vector%x
        y2=molecule(k)%y+Psep(i)*vect_u1(i)%y-Prot_sep*vector%y
        z2=molecule(k)%z+Psep(i)*vect_u1(i)%z-Prot_sep*vector%z

        call distance(x1,y1,z1,x2,y2,z2,dx,dy,dz,r2)
       
        r=sqrt(r2)
        rmin=min(rmin,r)

        if(r<sample_dist) then
          Psep(i)=Psep(i)+sample_dist-r
        end if
      end do
    end do
    if(Psep(i)==Prot_sep) Psep(i)=Psep(i)-rmin+sample_dist
  end do

  return

end subroutine get_Psep

end module korobov

