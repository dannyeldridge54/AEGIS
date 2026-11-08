    ! Two-field dark energy for the Twist (AEGIS UB-2): the Barbero-Immirzi axion-dilaton on a hyperbolic field space.
    ! Fields (reduced Planck units): chi = canonical dilaton (|phi| = exp(S chi), S = sqrt(2/3)), theta = BI angle.
    ! Field-space metric G = diag(1, F(chi)^2), F = F_P exp(lam chi / 2), lam = -2 sqrt(2/3) (fixed by the theory).
    ! Potential 8 pi G V = VA u(chi) + VL (1 - cos theta)^3, in 1/Mpc^2 (VA, VL set from Python in those units).
    !   var = 1: u = (p - 1) exp(6 p) / p^2            (GKY Kahler, constant W)
    !   var = 2: u = exp(kpar chi)                      (exponential, slope kappa = kpar)
    !   var = 3: u = (p - 1) exp((6 - 2 kpar) p) / p^2  (GKY with W = W0 exp(b Phi), b = kpar)
    ! The background (chi, theta and their conformal-time derivatives) is solved in Python on CAMB's own background
    ! (cmb-fit/ub2_fit.py) and passed in with SetTable; this module splines it and evolves the linear perturbations of
    ! BOTH fields in synchronous gauge (no fluid or PPF approximation):
    !   dchi'' = -2H dchi' - k z chi' - k^2 dchi + (lam/2)(lam F^2 th'^2 dchi + 2 F^2 th' dth') - a^2 (Vcc dchi + Vct dth)
    !   dth''  = -2H dth'  - k z th'  - k^2 dth  - lam (chi' dth' + th' dchi') - a^2 (Vtt dth + (Vct - lam Vt) dchi) / F^2
    !   a^2 8piG drho = chi' dchi' + F^2 th' dth' + (lam/2) F^2 th'^2 dchi + a^2 (Vc dchi + Vt dth)
    !   a^2 8piG (rho+p) v = k (chi' dchi + F^2 th' dth)
    ! Single-field limit (no theta) reduces exactly to CAMB's TQuintessence equations.

    module UBField
    use DarkEnergyInterface
    use results
    use constants
    use classes
    use Interpolation, only: spline
    implicit none
    private

    real(dl), parameter :: S_dil = 0.816496580927726_dl ! sqrt(2/3)

    type, extends(TDarkEnergyModel) :: TUBField
        real(dl) :: VA = 0._dl, VL = 0._dl, kpar = 0._dl
        real(dl) :: FP = 1.5593936_dl, lam = -1.632993161855452_dl
        integer :: var = 2, ntab = 0
        real(dl), allocatable :: loga(:), chi(:), th(:), chip(:), thp(:)
        real(dl), allocatable :: d2chi(:), d2th(:), d2chip(:), d2thp(:)
    contains
    procedure :: Init => TUBField_Init
    procedure :: BackgroundDensityAndPressure => TUBField_BackgroundDensityAndPressure
    procedure :: PerturbedStressEnergy => TUBField_PerturbedStressEnergy
    procedure :: PerturbationEvolve => TUBField_PerturbationEvolve
    procedure :: SetTable => TUBField_SetTable
    procedure, nopass :: PythonClass => TUBField_PythonClass
    procedure, nopass :: SelfPointer => TUBField_SelfPointer
    end type TUBField

    public TUBField

    contains

    subroutine TUBField_SetTable(this, loga, chi, th, chip, thp, n)
    class(TUBField) :: this
    integer, intent(in) :: n
    real(dl), intent(in) :: loga(n), chi(n), th(n), chip(n), thp(n)

    if (abs(loga(n)) > 1e-6_dl) error stop 'UB field table must end at a = 1'
    this%ntab = n
    if (allocated(this%loga)) deallocate(this%loga, this%chi, this%th, this%chip, this%thp, &
        this%d2chi, this%d2th, this%d2chip, this%d2thp)
    allocate(this%loga(n), this%chi(n), this%th(n), this%chip(n), this%thp(n))
    allocate(this%d2chi(n), this%d2th(n), this%d2chip(n), this%d2thp(n))
    this%loga = loga
    this%chi = chi
    this%th = th
    this%chip = chip
    this%thp = thp
    call spline(this%loga, this%chi, n, 1d30, 1d30, this%d2chi)
    call spline(this%loga, this%th, n, 1d30, 1d30, this%d2th)
    call spline(this%loga, this%chip, n, 1d30, 1d30, this%d2chip)
    call spline(this%loga, this%thp, n, 1d30, 1d30, this%d2thp)

    end subroutine TUBField_SetTable

    subroutine TUBField_Init(this, State)
    class(TUBField), intent(inout) :: this
    class(TCAMBdata), intent(in), target :: State

    if (this%ntab < 2) error stop 'TUBField: call SetTable before use'
    this%is_cosmological_constant = .false.
    this%num_perturb_equations = 4

    end subroutine TUBField_Init

    subroutine TUBField_BackgroundDensityAndPressure(this, grhov, a, grhov_t, w)
    ! grhov_t = 8 pi G rho_de a^2 and (optionally) w
    class(TUBField), intent(inout) :: this
    real(dl), intent(in) :: grhov, a
    real(dl), intent(out) :: grhov_t
    real(dl), intent(out), optional :: w
    real(dl) :: chi, th, chip, thp, F2, kin, a2V, V, Vc, Vt, Vcc, Vct, Vtt

    call TUBField_Vals_in(this, a, chi, th, chip, thp)
    call TUBField_Pot_in(this, chi, th, V, Vc, Vt, Vcc, Vct, Vtt)
    F2 = (this%FP*exp(this%lam*chi/2))**2
    kin = (chip**2 + F2*thp**2)/2
    a2V = a**2*V
    grhov_t = kin + a2V
    if (present(w)) then
        if (grhov_t > 0) then
            w = (kin - a2V)/grhov_t
        else
            w = -1
        end if
    end if

    end subroutine TUBField_BackgroundDensityAndPressure

    subroutine TUBField_PerturbedStressEnergy(this, dgrhoe, dgqe, &
        a, dgq, dgrho, grho, grhov_t, w, gpres_noDE, etak, adotoa, k, kf1, ay, ayprime, w_ix)
    class(TUBField), intent(inout) :: this
    real(dl), intent(out) :: dgrhoe, dgqe
    real(dl), intent(in) :: a, dgq, dgrho, grho, grhov_t, w, gpres_noDE, etak, adotoa, k, kf1
    real(dl), intent(in) :: ay(*)
    real(dl), intent(inout) :: ayprime(*)
    integer, intent(in) :: w_ix
    real(dl) :: chi, th, chip, thp, F2, V, Vc, Vt, Vcc, Vct, Vtt, dc, dcp, dt, dtp

    call TUBField_Vals_in(this, a, chi, th, chip, thp)
    call TUBField_Pot_in(this, chi, th, V, Vc, Vt, Vcc, Vct, Vtt)
    F2 = (this%FP*exp(this%lam*chi/2))**2
    dc = ay(w_ix); dcp = ay(w_ix + 1); dt = ay(w_ix + 2); dtp = ay(w_ix + 3)
    dgrhoe = chip*dcp + F2*thp*dtp + this%lam/2*F2*thp**2*dc + a**2*(Vc*dc + Vt*dt)
    dgqe = k*(chip*dc + F2*thp*dt)

    end subroutine TUBField_PerturbedStressEnergy

    subroutine TUBField_PerturbationEvolve(this, ayprime, w, w_ix, a, adotoa, k, z, y)
    class(TUBField), intent(in) :: this
    real(dl), intent(inout) :: ayprime(:)
    real(dl), intent(in) :: a, adotoa, w, k, z, y(:)
    integer, intent(in) :: w_ix
    real(dl) :: chi, th, chip, thp, F2, V, Vc, Vt, Vcc, Vct, Vtt, dc, dcp, dt, dtp, lam

    call TUBField_Vals_in(this, a, chi, th, chip, thp)
    call TUBField_Pot_in(this, chi, th, V, Vc, Vt, Vcc, Vct, Vtt)
    lam = this%lam
    F2 = (this%FP*exp(lam*chi/2))**2
    dc = y(w_ix); dcp = y(w_ix + 1); dt = y(w_ix + 2); dtp = y(w_ix + 3)
    ayprime(w_ix) = dcp
    ayprime(w_ix + 1) = -2*adotoa*dcp - k*z*chip - k**2*dc + lam/2*(lam*F2*thp**2*dc + 2*F2*thp*dtp) &
        - a**2*(Vcc*dc + Vct*dt)
    ayprime(w_ix + 2) = dtp
    ayprime(w_ix + 3) = -2*adotoa*dtp - k*z*thp - k**2*dt - lam*(chip*dtp + thp*dcp) &
        - a**2*(Vtt*dt + (Vct - lam*Vt)*dc)/F2

    end subroutine TUBField_PerturbationEvolve

    subroutine TUBField_Vals_in(this, a, chi, th, chip, thp)
    class(TUBField), intent(in) :: this
    real(dl), intent(in) :: a
    real(dl), intent(out) :: chi, th, chip, thp
    real(dl) :: x, h, aa, bb
    integer :: lo, hi, mid

    x = log(a)
    if (x <= this%loga(1)) then
        chi = this%chi(1); th = this%th(1); chip = 0; thp = 0
        return
    end if
    if (x >= this%loga(this%ntab)) then
        chi = this%chi(this%ntab); th = this%th(this%ntab)
        chip = this%chip(this%ntab); thp = this%thp(this%ntab)
        return
    end if
    lo = 1
    hi = this%ntab
    do while (hi - lo > 1)
        mid = (lo + hi)/2
        if (this%loga(mid) > x) then
            hi = mid
        else
            lo = mid
        end if
    end do
    h = this%loga(hi) - this%loga(lo)
    aa = (this%loga(hi) - x)/h
    bb = 1 - aa
    chi = aa*this%chi(lo) + bb*this%chi(hi) + ((aa**3 - aa)*this%d2chi(lo) + (bb**3 - bb)*this%d2chi(hi))*h**2/6
    th = aa*this%th(lo) + bb*this%th(hi) + ((aa**3 - aa)*this%d2th(lo) + (bb**3 - bb)*this%d2th(hi))*h**2/6
    chip = aa*this%chip(lo) + bb*this%chip(hi) + ((aa**3 - aa)*this%d2chip(lo) + (bb**3 - bb)*this%d2chip(hi))*h**2/6
    thp = aa*this%thp(lo) + bb*this%thp(hi) + ((aa**3 - aa)*this%d2thp(lo) + (bb**3 - bb)*this%d2thp(hi))*h**2/6

    end subroutine TUBField_Vals_in

    subroutine TUBField_Pot_in(this, chi, th, V, Vc, Vt, Vcc, Vct, Vtt)
    class(TUBField), intent(in) :: this
    real(dl), intent(in) :: chi, th
    real(dl), intent(out) :: V, Vc, Vt, Vcc, Vct, Vtt
    real(dl) :: c, s, om, h, k, p, e
    real(dl) :: d1, d2

    c = cos(th)
    s = sin(th)
    om = 1 - c
    Vt = this%VL*3*om**2*s
    Vtt = this%VL*3*(2*om*s**2 + om**2*c)
    Vct = 0
    if (this%var == 2) then
        V = this%VA*exp(this%kpar*chi) + this%VL*om**3
        Vc = this%VA*this%kpar*exp(this%kpar*chi)
        Vcc = this%VA*this%kpar**2*exp(this%kpar*chi)
    else
        k = 6._dl
        if (this%var == 3) k = 6._dl - 2*this%kpar
        p = exp(S_dil*chi)
        e = exp(k*p)/p**2
        V = this%VA*(p - 1)*e + this%VL*om**3
        Vc = this%VA*e*(1 + (p - 1)*(k - 2/p))*S_dil*p
        h = 1d-5*max(1._dl, abs(chi))
        d1 = gk_d(chi + h, k)
        d2 = gk_d(chi - h, k)
        Vcc = this%VA*(d1 - d2)/(2*h)
    end if

    end subroutine TUBField_Pot_in

    real(dl) function gk_d(chi, k)
    real(dl), intent(in) :: chi, k
    real(dl) :: p, e

    p = exp(S_dil*chi)
    e = exp(k*p)/p**2
    gk_d = e*(1 + (p - 1)*(k - 2/p))*S_dil*p

    end function gk_d

    function TUBField_PythonClass()
    character(len=:), allocatable :: TUBField_PythonClass

    TUBField_PythonClass = 'UBField'

    end function TUBField_PythonClass

    subroutine TUBField_SelfPointer(cptr, P)
    use iso_c_binding
    type(c_ptr) :: cptr
    type(TUBField), pointer :: PType
    class(TPythonInterfacedClass), pointer :: P

    call c_f_pointer(cptr, PType)
    P => PType

    end subroutine TUBField_SelfPointer

    end module UBField
