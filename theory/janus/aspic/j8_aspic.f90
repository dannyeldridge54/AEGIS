program j8
  use infprec, only : kp
  use cosmopar, only : powerAmpScalar
  use srreheat, only : Nzero
  use srflow, only : scalar_spectral_index, tensor_to_scalar_ratio, scalar_running
  use dwisr, only : dwi_x_endinf, dwi_epsilon_one, dwi_epsilon_two, dwi_epsilon_three
  use dwireheat, only : dwi_x_star
  use esisr, only : esi_x_endinf, esi_epsilon_one, esi_epsilon_two, esi_epsilon_three
  use esireheat, only : esi_x_star
  use lfisr, only : lfi_x_endinf, lfi_epsilon_one, lfi_epsilon_two, lfi_epsilon_three
  use lfireheat, only : lfi_x_star
  use lisr, only : li_x_endinf, li_epsilon_one, li_epsilon_two, li_epsilon_three
  use lireheat, only : li_x_star
  use mhisr, only : mhi_x_endinf, mhi_epsilon_one, mhi_epsilon_two, mhi_epsilon_three
  use mhireheat, only : mhi_x_star
  use nisr, only : ni_x_endinf, ni_epsilon_one, ni_epsilon_two, ni_epsilon_three
  use nireheat, only : ni_x_star
  use rgisr, only : rgi_x_endinf, rgi_epsilon_one, rgi_epsilon_two, rgi_epsilon_three
  use rgireheat, only : rgi_x_star
  use sfisr, only : sfi_x_endinf, sfi_epsilon_one, sfi_epsilon_two, sfi_epsilon_three
  use sfireheat, only : sfi_x_star
  use sisr, only : si_x_endinf, si_epsilon_one, si_epsilon_two, si_epsilon_three
  use sireheat, only : si_x_star
  implicit none
  real(kp) :: LR(2) = (/-100._kp, -150._kp/), x, xe, e(3), bf, P
  integer :: i, j
  P = powerAmpScalar
  write(*,'(A,ES24.16)') 'NZERO ', Nzero
  do i = 1, 17
  if (i == 9) cycle
  do j = 1, 2
  select case (i)
  case (1)
    xe = lfi_x_endinf(2._kp); x = lfi_x_star(2._kp,xe, 0._kp, LR(j), P, bf)
    e = (/lfi_epsilon_one(x,2._kp), lfi_epsilon_two(x,2._kp), lfi_epsilon_three(x,2._kp)/)
  case (2)
    xe = lfi_x_endinf(4._kp); x = lfi_x_star(4._kp,xe, 0._kp, LR(j), P, bf)
    e = (/lfi_epsilon_one(x,4._kp), lfi_epsilon_two(x,4._kp), lfi_epsilon_three(x,4._kp)/)
  case (3)
    xe = lfi_x_endinf(2._kp/3._kp); x = lfi_x_star(2._kp/3._kp,xe, 0._kp, LR(j), P, bf)
    e = (/lfi_epsilon_one(x,2._kp/3._kp), lfi_epsilon_two(x,2._kp/3._kp), lfi_epsilon_three(x,2._kp/3._kp)/)
  case (4)
    xe = si_x_endinf(); x = si_x_star(xe, 0._kp, LR(j), P, bf)
    e = (/si_epsilon_one(x), si_epsilon_two(x), si_epsilon_three(x)/)
  case (5)
    xe = ni_x_endinf(5._kp); x = ni_x_star(5._kp,xe, 0._kp, LR(j), P, bf)
    e = (/ni_epsilon_one(x,5._kp), ni_epsilon_two(x,5._kp), ni_epsilon_three(x,5._kp)/)
  case (6)
    xe = ni_x_endinf(10._kp); x = ni_x_star(10._kp,xe, 0._kp, LR(j), P, bf)
    e = (/ni_epsilon_one(x,10._kp), ni_epsilon_two(x,10._kp), ni_epsilon_three(x,10._kp)/)
  case (7)
    xe = esi_x_endinf(1._kp); x = esi_x_star(1._kp,xe, 0._kp, LR(j), P, bf)
    e = (/esi_epsilon_one(x,1._kp), esi_epsilon_two(x,1._kp), esi_epsilon_three(x,1._kp)/)
  case (8)
    xe = mhi_x_endinf(10._kp); x = mhi_x_star(10._kp,xe, 0._kp, LR(j), P, bf)
    e = (/mhi_epsilon_one(x,10._kp), mhi_epsilon_two(x,10._kp), mhi_epsilon_three(x,10._kp)/)
  case (10)
    xe = rgi_x_endinf(1._kp); x = rgi_x_star(1._kp,xe, 0._kp, LR(j), P, bf)
    e = (/rgi_epsilon_one(x,1._kp), rgi_epsilon_two(x,1._kp), rgi_epsilon_three(x,1._kp)/)
  case (11)
    xe = dwi_x_endinf(25._kp); x = dwi_x_star(25._kp,xe, 0._kp, LR(j), P, bf)
    e = (/dwi_epsilon_one(x,25._kp), dwi_epsilon_two(x,25._kp), dwi_epsilon_three(x,25._kp)/)
  case (12)
    xe = sfi_x_endinf(2._kp,20._kp); x = sfi_x_star(2._kp,20._kp,xe, 0._kp, LR(j), P, bf)
    e = (/sfi_epsilon_one(x,2._kp,20._kp), sfi_epsilon_two(x,2._kp,20._kp), sfi_epsilon_three(x,2._kp,20._kp)/)
  case (13)
    xe = li_x_endinf(0.3_kp); x = li_x_star(0.3_kp,xe, 0._kp, LR(j), P, bf)
    e = (/li_epsilon_one(x,0.3_kp), li_epsilon_two(x,0.3_kp), li_epsilon_three(x,0.3_kp)/)
  case (14)
    xe = esi_x_endinf(sqrt(2._kp)); x = esi_x_star(sqrt(2._kp),xe, 0._kp, LR(j), P, bf)
    e = (/esi_epsilon_one(x,sqrt(2._kp)), esi_epsilon_two(x,sqrt(2._kp)), esi_epsilon_three(x,sqrt(2._kp))/)
  case (15)
    xe = ni_x_endinf(7._kp); x = ni_x_star(7._kp,xe, 0._kp, LR(j), P, bf)
    e = (/ni_epsilon_one(x,7._kp), ni_epsilon_two(x,7._kp), ni_epsilon_three(x,7._kp)/)
  case (16)
    xe = lfi_x_endinf(3._kp); x = lfi_x_star(3._kp,xe, 0._kp, LR(j), P, bf)
    e = (/lfi_epsilon_one(x,3._kp), lfi_epsilon_two(x,3._kp), lfi_epsilon_three(x,3._kp)/)
  case (17)
    xe = lfi_x_endinf(1._kp); x = lfi_x_star(1._kp,xe, 0._kp, LR(j), P, bf)
    e = (/lfi_epsilon_one(x,1._kp), lfi_epsilon_two(x,1._kp), lfi_epsilon_three(x,1._kp)/)
  end select
  write(*,'(I3,1X,F6.1,1X,ES22.14,1X,ES22.14,1X,ES22.14,1X,ES22.14,1X,ES22.14)') i, LR(j), -bf, &
     scalar_spectral_index(e), tensor_to_scalar_ratio(e), scalar_running(e), x
  end do
  end do
end program j8
