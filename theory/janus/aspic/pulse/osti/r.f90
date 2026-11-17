program pr
  use infprec, only : kp
  use srflow, only : scalar_spectral_index, tensor_to_scalar_ratio, scalar_running
  use srreheat, only : Nzero
  use ostisr
  use ostireheat
  implicit none
  real(kp) :: x, xe, e(3), bf, P
  P = 2.1127e-9_kp; xe = osti_x_endinf(100._kp)
  write(*,'(A,ES24.16)') 'NZ ', Nzero
  x = osti_x_rrad(100._kp,xe, 0._kp, P, bf); e = (/osti_epsilon_one(x,100._kp), osti_epsilon_two(x,100._kp), osti_epsilon_three(x,100._kp)/)
  write(*,'(A,A,F7.1,5ES24.15)') 'RT ', 'rrad ', 0.0, -bf, scalar_spectral_index(e), tensor_to_scalar_ratio(e), scalar_running(e), x
  x = osti_x_rrad(100._kp,xe, -10._kp, P, bf); e = (/osti_epsilon_one(x,100._kp), osti_epsilon_two(x,100._kp), osti_epsilon_three(x,100._kp)/)
  write(*,'(A,A,F7.1,5ES24.15)') 'RT ', 'rrad ', -10.0, -bf, scalar_spectral_index(e), tensor_to_scalar_ratio(e), scalar_running(e), x
  x = osti_x_star(100._kp,xe, 0._kp, -100._kp, P, bf); e = (/osti_epsilon_one(x,100._kp), osti_epsilon_two(x,100._kp), osti_epsilon_three(x,100._kp)/)
  write(*,'(A,A,F7.1,5ES24.15)') 'RT ', 'rhow ', -100.0, -bf, scalar_spectral_index(e), tensor_to_scalar_ratio(e), scalar_running(e), x
  x = osti_x_star(100._kp,xe, 0._kp, -150._kp, P, bf); e = (/osti_epsilon_one(x,100._kp), osti_epsilon_two(x,100._kp), osti_epsilon_three(x,100._kp)/)
  write(*,'(A,A,F7.1,5ES24.15)') 'RT ', 'rhow ', -150.0, -bf, scalar_spectral_index(e), tensor_to_scalar_ratio(e), scalar_running(e), x
end program pr
