program pp
  use infprec, only : kp
  use srflow, only : scalar_spectral_index, tensor_to_scalar_ratio, scalar_running
  use saaisr
  implicit none
  real(kp) :: Ns(2) = (/50._kp, 60._kp/), x, xe, e(3), x60, xf, xx
  integer :: j, k
  xe = saai_x_endinf(2._kp)
  do j = 1, 2
    x = saai_x_trajectory(-Ns(j), xe,2._kp); if (j == 2) x60 = x
    e = (/saai_epsilon_one(x,2._kp), saai_epsilon_two(x,2._kp), saai_epsilon_three(x,2._kp)/)
    write(*,'(A,F5.1,6ES24.15)') 'PT ', Ns(j), x, scalar_spectral_index(e), tensor_to_scalar_ratio(e), scalar_running(e), xe, e(1)
  end do
  xf = x60 + 4._kp*(x60 - xe)
  do k = 0, 3999
    xx = xe + (xf - xe)*real(k,kp)/3999._kp
    write(*,'(A,3ES24.15)') 'VG ', xx, saai_norm_potential(xx,2._kp), saai_norm_deriv_potential(xx,2._kp)
  end do
end program pp
