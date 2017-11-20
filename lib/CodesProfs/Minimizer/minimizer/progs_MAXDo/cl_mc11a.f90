module clean_mc11a

  use particles

  implicit none

  contains 

subroutine mc11a(a,n,z,sig,w,ir,mk,eps)
!======================================

  integer, intent(IN) :: n,mk
  integer,intent(INOUT) :: ir
  integer :: np,ij,i,ip,j,mm

  real(8),intent(IN) :: sig,eps
  
  real(8) ::  ti,v,tim,al,r,b,gm,y  

  real(8), intent(INOUT), dimension(Ntot) :: a
  real(8), intent(INOUT), dimension(Nvar) :: z,w

  if(n>1) goto 1  
  a(1)=a(1)+sig*(z(1)**2)
  ir=1
  if(a(1)>0.d0) return
  a(1)=0.d0
  ir=0 

  return

1 continue
  np=n+1
  if(sig>0.d0) goto 40
  if(sig==0.d0.or.ir==0) return
  ti=1.d0/sig
  ij=1
  if(mk==0) goto 10

  do i=1,n
    if(a(ij)/=0.d0) ti=ti+(w(i)**2)/a(ij)
    ij=ij+np-i 
  end do

  goto 20
10 continue     
  w(1:n)=z(1:n) 

  do i=1,n
    ip=i+1
    v=w(i)
    if(a(ij)>0.d0) goto 12
    w(i)=0.d0
    ij=ij+np-i
    cycle

12 continue 
    ti=ti+v**2/a(ij)

    if(i==n) goto 14
       
    do j=ip,n 
      ij=ij+1 
      w(j)=w(j)-v*a(ij)
    end do
 
14  ij=ij+1       
  end do

20 continue
  if(ir<=0) goto 21
  if(ti>0.d0) goto 22
  if(mk-1<=0) then
    go to 40
  else
    go to 23 
  end if
21 ti=0.d0
  ir=-ir-1  
  go to 23
22 ti=eps/sig 
  if(eps==0.d0) ir=ir-1  
23 continue
  mm=1
  tim=ti
  
  do i=1,n  
    j=np-i
    ij=ij-i
    if(a(ij)/=0.d0) tim=ti-(w(j)**2)/a(ij)
    w(j)=ti
    ti=tim 
  end do

  goto 41

40 continue
  mm=0
  tim=1.d0/sig
41 continue
  ij=1 

  do i=1,n
    ip=i+1
    v=z(i)
    if(a(ij)>0.d0) goto 53
    if(ir>0.or.sig<0.d0.or.v==0.d0) goto 52
    ir=1-ir
    a(ij)=v**2/tim
    if(i==n) return

    do j=ip,n
      ij=ij+1
      a(ij)=z(j)/v
    end do 

    return
52  continue
    ti=tim
    ij=ij+n-i
    cycle
53  continue
    al=v/a(ij)
   
    if(mm<=0) then
      ti=tim+v*al
    else
       ti=w(i)
    end if 

    r=ti/tim
    a(ij)=a(ij)*r
    if(r==0.d0.or.i==n) exit   
    b=al/ti
    if(r>4.d0) goto 62 

    do j=ip,n
      ij=ij+1
      z(j)=z(j)-v*a(ij)
      a(ij)=a(ij)+b*z(j)
    end do

    goto 64  
62  gm=tim/ti
    
    do j=ip,n
      ij=ij+1
      y=a(ij)
      a(ij)=b*z(j)+y*gm
      z(j)=z(j)-v*y
    end do     

64  continue
    tim=ti
    ij=ij+1
  end do

  if(ir<0) ir=-ir

  return

end subroutine mc11a

!-----------------------------------multiply vector z by inverse of factors in a
subroutine mc11e(a,n,z,w,ir)
!===========================

  integer, intent(IN) :: n,ir

  integer :: i,ij,i1,j,np,nip,ii,ip

  real(8), intent(INOUT), dimension(Nvar) :: z,w
  real(8), intent(IN), dimension(Ntot) :: a

  real(8) ::  v

  if(ir<n) return
  w(1)=z(1)
  if(n>1) goto 400
  z(1)=z(1)/a(1)
  
  return

400 continue

  do i=2,n
    ij=i  
    i1=i-1
    v=z(i)
 
    do j=1,i1
      v=v-a(ij)*z(j)
      ij=ij+n-j
    end do

    w(i)=v
    z(i)=v
  end do

  z(n)=z(n)/a(ij)
  np=n+1  

  do nip=2,n
    i=np-nip
    ii=ij-nip
    v=z(i)/a(ii)
    ip=i+1 
    ij=ii
    
    do j=ip,n
      ii=ii+1
      v=v-a(ii)*z(j)
    end do

    z(i)=v 
  end do

  return

end subroutine mc11e

end module clean_mc11a
