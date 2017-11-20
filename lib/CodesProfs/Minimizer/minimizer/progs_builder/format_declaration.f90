module format_declaration
  
  implicit none
   
  character*60 :: form_date="(1x,a24,i2,a1,i2,a1,i4,a4,i2,a1,i2,a1,i2,a10)"
  
  character*40 :: form_file="(1x,a22,1x,a40)"
  character*40 :: form_i   ="(1x,20i7)"
  character*40 :: form_r   ="(1x,20f13.6)"
!  character*40 :: form_glob="(1x,i4,1x,i6,1x,18f13.6)"
  character*40 :: form_glob="(1x,i4,i4,1x,18f13.6)"
  character*40 :: form_c1  ="(1x,a52)"
  character*40 :: form_c2  ="(1x,a21)"
  
  character*70 :: form_i_loop="(1x,a32,2x,i10,a7,i2,a1,i2,a1,i4,a7,i2,a1,i2,a1,i2)"

  character*40 :: form_mean="(1x,a32,1x,f12.5)"
  character*40 :: form_tens="(1x,a40,1x,3f12.5)"
  character*40 :: form_talp="(1x,a35,1x,3es15.5)"

  character*80 :: form_end="(1x,a75)"
  
  character*40 :: form_text="(1x,a64)"
  character*40 :: form_pari="(1x,a30,i10,a24)"
  character*40 :: form_parr="(1x,a30,f10.5,a24)"
  character*40 :: form_g   ="(1x,4g15.7)"
  
  character*80 :: form_L1="(a5,2x,f7.3,2x,f7.3,2x,f7.3,2x,a24)"
  character*80 :: form_L2="(a4,i5,2x,a2,15x,3f8.3,16x,a2)"

 ! character*80 :: form_pdb    ="(6x,i5,2x,a3,1x,a4,a1,i4,4x,3f8.3)"
 ! Modification by Lydie 20/03/15
  character*80 :: form_pdb    ="(6x,i5,2x,a3,1x,a4,a1,i4,a1,3x,3f8.3)"
  character*80 :: form_res    ="(13x,a3,1x,a4,a1,i4)"
  character*80 :: form_ato    ="(6x,i5,2x,a3,6x,i4,4x,3f8.3)"
  character*80 :: form_coord  ="(30x,3f8.3)"
  character*80 :: form_chain  ="(a3,3x,i5,6x,a4,a1,i4)"
!  character*80 :: form_prot   ="(a4,2x,i5,2x,a3,1x,a4,a1,i4,4x,3f8.3)"
! Modification by Lydie 20/03/15
  character*80 :: form_prot   ="(a4,2x,i5,2x,a3,1x,a4,a1,i4,a1,3x,3f8.3)"
  character*80 :: form_line   ="(a)"
  character*80 :: form_endpdb ="(a4,13x,a4,1x,i4)"
  character*80 :: form_final  ="(17x,a4,10x,f6.2)"
  character*90 :: form_min   ="(a6,1x,a6,1x,i5,1x,3f13.6,i5,1x,f13.6,i5,1x,8f13.6)"

end module format_declaration
