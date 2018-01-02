module getmin

  use run_parameter
  use particles
  use proteins
  use microb
  use springs
  use energa
  use clean_minfor
  use timing

  implicit none

contains

subroutine minimize(Efinal,Elj,Eelec)
!====================================

  integer :: Npart,prot
  integer :: iter,niter
  integer :: part1,part2, ic, i
  integer :: nd,nw,nxa,nga,nxb,ngb
  integer :: sep,rot,gam

  real(8), intent(OUT) :: Efinal,Elj,Eelec

  real(8) ::  Etot,Estart,Eend
  real(8) ::  elapsed_CPU_time
 
  real(8), dimension(6) :: grad, scal, refpos,refgrad
  real(8), dimension(n7*(n7+13)/2) :: work

  character*50 pdb_name

  pdb_name='minim'

  Nvar=6
  Ntot=n7*(n7+13)/2

  Eold=0.0d0
  Estart=0.0d0
  Efinal=0.0d0
  work(:)=0.0d0
  grad(:)=0.0d0
  
  scal(1:3)=0.1d0
  scal(4:6)=1.5d0
  
  scal(:)=scal(:)*stpfac

  nd=1+(Nvar*(Nvar+1))/2
  nw=nd+Nvar
  nxa=nw+Nvar
  nga=nxa+Nvar
  nxb=nga+Nvar
  ngb=nxb+Nvar

!  call start_rotation(Lig_position)
  write(6,form_r) Lig_position(1),Lig_position(2),Lig_position(3),Lig_position(6),Lig_position(4),Lig_position(5)
  refpos=Lig_position  

  call energy(Lig_position,Estart,Elj,Eelec,grad)
  refgrad=grad
  evalf_number=evalf_number+1
  write(6,form_tens) 'Starting energy ', Estart
  write(6,form_talp) 'Starting forces ', grad(1), grad(2), grad(3)
  write(6,form_talp) 'Starting moments', grad(4), grad(5), grad(6)
  write(6,*)

  Eold=Estart
  Etot=Estart

  write(6,form_text) 'calling minimizer'
  write(6,form_text) 'minimizing with simple(Zacharias) potential' 
  call minfor(Nvar,Lig_position,Etot,grad,scal,gtol,work,work(nd:),work(nw:),work(nxa:),work(nga:),work(nxb:),work(ngb:), &
  maxiter,niter)
  Efinal=Etot
  if(niter==maxiter) then
    write(6,*) 'iterations limit, minimization failed'
    Efinal=Estart
    Lig_position=refpos
    grad=refgrad

    return
  end if  

  write(6,form_tens) 'End of minimization', real(niter), Efinal, Estart
  write(6,form_r) grad(1), grad(2), grad(3), grad(6), grad(4), grad(5)  
  write(6,form_r) Lig_position(1),Lig_position(2),Lig_position(3),Lig_position(6),Lig_position(4),Lig_position(5)

  Eend=Efinal

  if(abs(maxval(grad))>5.0*gtol.or.abs(minval(grad))>5.0*gtol) then
    write(6,*) 'Minimisation failure, forces to high'
    Efinal=0.0d0
    Elj=0.d0
    Eelec=0.d0
  else   
    call get_centers(.true.)
    call energy(Lig_position,Efinal,Elj,Eelec,grad)
    evalf_number=evalf_number+1
!    call write_pdb_file(2,pdb_name)
    if(abs(Efinal-Eend)>0.1d0)then
      write(6,form_tens) 'Suspicious energy change', Eend, Efinal
      Efinal=0.d0
    else if(Prot_sep>1000.d0) then
      write(6,form_tens) 'Ligand rejected', Prot_sep
      Efinal=0.d0 
    end if
  end if

  elapsed_CPU_time=elapsed_time()
  write(6 ,form_talp) 'CPU time elapsed since start : ',elapsed_CPU_time
  write(6,*) 

  return

end subroutine minimize

end module getmin
