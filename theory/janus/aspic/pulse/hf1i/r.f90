program pr
  use infprec, only : kp
  use srflow, only : scalar_spectral_index, tensor_to_scalar_ratio, scalar_running
  use srreheat, only : Nzero
  use hf1isr
  use hf1ireheat
  implicit none
  real(kp) :: x, xe, e(3), bf, P
  P = 2.1127e-9_kp; xe = hf1i_x_endinf(0.1_kp)
  write(*,'(A,ES24.16)') 'NZ ', Nzero
  x = hf1i_x_rrad(0.1_kp,xe, 0._kp, P, bf); e = (/hf1i_epsilon_one(x,0.1_kp), hf1i_epsilon_two(x,0.1_kp), hf1i_epsilon_three(x,0.1_kp)/)
  write(*,'(A,A,F7.1,5ES24.15)') 'RT ', 'rrad ', 0.0, -bf, scalar_spectral_index(e), tensor_to_scalar_ratio(e), scalar_running(e), x
  x = hf1i_x_rrad(0.1_kp,xe, -10._kp, P, bf); e = (/hf1i_epsilon_one(x,0.1_kp), hf1i_epsilon_two(x,0.1_kp), hf1i_epsilon_three(x,0.1_kp)/)
  write(*,'(A,A,F7.1,5ES24.15)') 'RT ', 'rrad ', -10.0, -bf, scalar_spectral_index(e), tensor_to_scalar_ratio(e), scalar_running(e), x
  x = hf1i_x_star(0.1_kp,xe, 0._kp, -100._kp, P, bf); e = (/hf1i_epsilon_one(x,0.1_kp), hf1i_epsilon_two(x,0.1_kp), hf1i_epsilon_three(x,0.1_kp)/)
  write(*,'(A,A,F7.1,5ES24.15)') 'RT ', 'rhow ', -100.0, -bf, scalar_spectral_index(e), tensor_to_scalar_ratio(e), scalar_running(e), x
  x = hf1i_x_star(0.1_kp,xe, 0._kp, -150._kp, P, bf); e = (/hf1i_epsilon_one(x,0.1_kp), hf1i_epsilon_two(x,0.1_kp), hf1i_epsilon_three(x,0.1_kp)/)
  write(*,'(A,A,F7.1,5ES24.15)') 'RT ', 'rhow ', -150.0, -bf, scalar_spectral_index(e), tensor_to_scalar_ratio(e), scalar_running(e), x
end program pr
