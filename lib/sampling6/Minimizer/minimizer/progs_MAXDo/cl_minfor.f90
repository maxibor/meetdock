module clean_minfor
 
  use particles
  use energa
  use clean_mc11a

  implicit none

  contains 

subroutine minfor(n,x,f,g,scal,acc,h,d,w,xa,ga,xb,gb,maxfun,nfun)
!================================================================

  integer, intent(IN) :: n,maxfun

  integer,intent(OUT) :: nfun

  integer :: itr,np,k,isfv,ir,i

  real(8),dimension(Nvar),intent(INOUT) :: x
  real(8),dimension(Nvar) ::g,scal
  real(8),dimension(Ntot) :: h
  real(8),dimension(Nvar) :: d,w,xa,ga,xb,gb
 
  real(8), intent(IN) :: acc
  real(8) ::  f

  real(8) ::  c,dff,fa,dga,stmin,step,stepbd,steplb
  real(8) ::  fmin,gmin,fb,dgb,gl1,gl2

  nfun=0
  itr=0
  np=n+1

!   set the hessian to a diagonal matrix depending on scal(.)
  c=0.d0

  do i=1,n
    c=max(c,abs(g(i)*scal(i)))
  end do

  if(c<=0.d0) c=1.d0
  k=(n*np)/2

  do i=1,k
    h(i)=0.d0
  end do

  k=1

  do i=1,n
    h(k)=0.01d0*c/(scal(i)**2)
    k=k+np-i
  end do

!   set some variables for the first iteration
     dff=0.d0
110  fa=f  
     isfv=1
     xa(1:n)=x(1:n)
     ga(1:n)=g(1:n)        
!   begin the iteration by giving the required printing
130  itr=itr+1     
!   calculate the search direction of the iteration
   do i=1,n
     d(i)=-ga(i)
   end do
   call mc11e(h,n,d,w,n)   
!   calculate a lower bound on the step-length and the initial directional derivative
   c=0.d0
   dga=0.d0

   do i=1,n
     c=max(c,abs(d(i)/scal(i)))
     dga=dga+ga(i)*d(i)
   end do
!   test if the search direction is downhill
   if(dga>=0.d0) goto 240  
!   set the initial step-length of the line search
   stmin=0.d0
   stepbd=0.d0
   steplb=acc/c
   fmin=fa
   gmin=dga
   step=1.d0
   if(dff<=0.d0) then
     step=min(step,1.0/c)
   else    
     step=min(step,(dff+dff)/(-dga))
   end if
170  c=stmin+step  
!   test whether func has been called maxfun times
   if(nfun>=maxfun) go to 250
   nfun=nfun+1
!   calculate another function value and gradient
   xb(1:n)=xa(1:n)+c*d(1:n)
   call move(nfun,xb,fb,gb)
!   store this function value if it is the smallest so far
   isfv=min(2,isfv)
   if(fb>f) goto 220
   if(fb<f) goto 200
   gl1=0.d0
   gl2=0.d0

   do i=1,n
     gl1=gl1+(scal(i)*g(i))**2
     gl2=gl2+(scal(i)*gb(i))**2
   end do   
 
   if(gl2>=gl1) goto 220
200  isfv=3   
   f=fb
   x(1:n)=xb(1:n)
   g(1:n)=gb(1:n)  
!   calculate the directional derivative at the new point
220  dgb=0.d0
   do i=1,n
     dgb=dgb+gb(i)*d(i)
   end do
!   branch if we have found a new lower bound on the step-length
   if(fb-fa<=0.1d0*c*dga) goto 280
!   finish the iteration if the current step is steplb
   if(step>steplb) goto 270 
240  if(isfv>=2) goto 110
!   at this stage the whole calculation is complete
250  if(nfun<maxfun) then
       nfun=nfun+1
       write(6,form_tens) 'calling move final', real(nfun)
       call move(nfun,x,f,g)
     endif
   return
!   calculate a new step-length by cubic interpolation
270  stepbd=step
   c=gmin+dgb-3.d0*(fb-fmin)/step
   c=gmin/(c+gmin-sqrt(c*c-gmin*dgb))
   step=step*max(0.1d0,c)
   goto 170
!   set the new bounds on the step-length
280  stepbd=stepbd-step
   stmin=c
   fmin=fb
   gmin=dgb
!   calculate a new step-length by extrapolation
   step=9.d0*stmin
   if(stepbd>0.d0) step=0.5d0*stepbd
   c=dga+3.d0*dgb-4.d0*(fb-fa)/stmin
   if(c>0.d0) step=min(step,stmin*max(1.0d0,-dgb/c))
   if(dgb<0.7d0*dga) goto 170
!   test for convergence of the iterations
   isfv=4-isfv  
   if(stmin+step<=steplb) goto 240 
!   revise the second derivative matrix
   ir=-n
   xa(1:n)=xb(1:n)
   xb(1:n)=ga(1:n)
   d(1:n)=gb(1:n)-ga(1:n)  
   ga(1:n)=gb(1:n)
   call mc11a(h,n,xb,1.d0/dga,w,ir,1,0.d0)
   ir=-ir
   call mc11a(h,n,d,1.d0/(stmin*(dgb-dga)),d,ir,0,0.d0) 
!   branch if the rank of the new matrix is deficient
   if(ir<n) goto 250
!   begin another iteration
   dff=fa-fb
   fa=fb
   goto 130

  return

end subroutine minfor

end module clean_minfor
