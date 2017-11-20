!This is the main program for ART current version 2001
!
! Copyright Normand Mousseau, May 2001
Module art_pro

  use run_parameter
  use particles
  use find_saddle_pro
  use energa
  use format_declaration
  use getmin
  use random

  implicit none

  contains

subroutine art_protein(etot,elj,elec)
!====================================

  integer :: niter,nac
  real(8) :: etot,elj,elec,estart
  real(8), dimension(Nvar) :: del_pos,force,grad 
  real(8) :: ftot2,ftot
  real(8) :: amin,bmin,gmin
  real(8) :: delpos2,difpos

  real(8), dimension(6) :: scal

  logical :: success

  scal(1:3)=1.d0
  scal(4:6)=15.d0

  call energy(Lig_position,estart,elj,elec,grad)
  evalf_number=evalf_number+1
  force=-grad

  write(6,form_tens) 'Starting Energy ', estart
  write(6,form_talp) 'Starting forces ', force(1),force(2),force(3)
  write(6,form_talp) 'Starting moments ', force(4),force(5),force(6)
   
  ftot2 = 0.0d0
  ftot2=dot_product(force,force)
  ftot=sqrt(ftot2)
  write(6,form_tens)'Total : ', ftot   

! We define the initial configuration as the reference configuration
  Lig_ref = Lig_position
  
  do niter=1,NUMBER_EVENTS    ! Main loop over the events
  ! We look for a local saddle point 
    do 
      call find_saddle( success )
      if ( success ) exit
    end do

! Push the configuration slightly over the saddle point in order to minimise 
! the odds that it falls back into its original state

    del_pos = Lig_position - Lig_ref
    delpos2=0.d0
    delpos2=dot_product(del_pos,del_pos)  
    difpos=sqrt(delpos2)

!    Lig_position = Lig_position + 0.2d0 * del_pos*scal
    Lig_position=Lig_position+0.15d0*difpos*projection*scal

    call minimize(etot,elj,elec)
    amin=Lig_position(6)
    bmin=Lig_position(4)
    gmin=Lig_position(5)

    ! Now, we accept or reject this move based on a Boltzmann weight
    if(etot-estart<-0.596*temp*log(ranval())) then
      nac=1
      write(6,*) 'New configuration accepted, iteration was : ', niter
      write(6,*)
      write(96,form_dec) nac, niter,Prot_sep,theta,phi,amin,bmin,gmin,elj,elec,etot

      ! We now redefine the reference configuration
      Lig_ref=Lig_position     ! This is a vectorial copy
      estart=etot
    else
      nac=0
      write(6,*) 'New configuration rejected, iteration was : ', niter
      write(6,*)
      write(96,form_dec) nac, niter,Prot_sep,theta,phi,amin,bmin,gmin,elj,elec,etot
    endif
  end do

  return

end subroutine art_protein

end module art_pro
