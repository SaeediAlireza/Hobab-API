#!/usr/bin/env python
#
# Hi There!
#
# You may be wondering what this giant blob of binary data here is, you might
# even be worried that we're up to something nefarious (good for you for being
# paranoid!). This is a base85 encoding of a zip file, this zip file contains
# an entire copy of pip (version 24.2).
#
# Pip is a thing that installs packages, pip itself is a package that someone
# might want to install, especially if they're looking to run this get-pip.py
# script. Pip has a lot of code to deal with the security of installing
# packages, various edge cases on various platforms, and other such sort of
# "tribal knowledge" that has been encoded in its code base. Because of this
# we basically include an entire copy of pip inside this blob. We do this
# because the alternatives are attempt to implement a "minipip" that probably
# doesn't do things correctly and has weird edge cases, or compress pip itself
# down into a single file.
#
# If you're wondering how this is created, it is generated using
# `scripts/generate.py` in https://github.com/pypa/get-pip.

import sys

this_python = sys.version_info[:2]
min_version = (3, 8)
if this_python < min_version:
    message_parts = [
        "This script does not work on Python {}.{}.".format(*this_python),
        "The minimum supported Python version is {}.{}.".format(*min_version),
        "Please use https://bootstrap.pypa.io/pip/{}.{}/get-pip.py instead.".format(*this_python),
    ]
    print("ERROR: " + " ".join(message_parts))
    sys.exit(1)


import os.path
import pkgutil
import shutil
import tempfile
import argparse
import importlib
from base64 import b85decode


def include_setuptools(args):
    """
    Install setuptools only if absent, not excluded and when using Python <3.12.
    """
    cli = not args.no_setuptools
    env = not os.environ.get("PIP_NO_SETUPTOOLS")
    absent = not importlib.util.find_spec("setuptools")
    python_lt_3_12 = this_python < (3, 12)
    return cli and env and absent and python_lt_3_12


def include_wheel(args):
    """
    Install wheel only if absent, not excluded and when using Python <3.12.
    """
    cli = not args.no_wheel
    env = not os.environ.get("PIP_NO_WHEEL")
    absent = not importlib.util.find_spec("wheel")
    python_lt_3_12 = this_python < (3, 12)
    return cli and env and absent and python_lt_3_12


def determine_pip_install_arguments():
    pre_parser = argparse.ArgumentParser()
    pre_parser.add_argument("--no-setuptools", action="store_true")
    pre_parser.add_argument("--no-wheel", action="store_true")
    pre, args = pre_parser.parse_known_args()

    args.append("pip")

    if include_setuptools(pre):
        args.append("setuptools")

    if include_wheel(pre):
        args.append("wheel")

    return ["install", "--upgrade", "--force-reinstall"] + args


def monkeypatch_for_cert(tmpdir):
    """Patches `pip install` to provide default certificate with the lowest priority.

    This ensures that the bundled certificates are used unless the user specifies a
    custom cert via any of pip's option passing mechanisms (config, env-var, CLI).

    A monkeypatch is the easiest way to achieve this, without messing too much with
    the rest of pip's internals.
    """
    from pip._internal.commands.install import InstallCommand

    # We want to be using the internal certificates.
    cert_path = os.path.join(tmpdir, "cacert.pem")
    with open(cert_path, "wb") as cert:
        cert.write(pkgutil.get_data("pip._vendor.certifi", "cacert.pem"))

    install_parse_args = InstallCommand.parse_args

    def cert_parse_args(self, args):
        if not self.parser.get_default_values().cert:
            # There are no user provided cert -- force use of bundled cert
            self.parser.defaults["cert"] = cert_path  # calculated above
        return install_parse_args(self, args)

    InstallCommand.parse_args = cert_parse_args


def bootstrap(tmpdir):
    monkeypatch_for_cert(tmpdir)

    # Execute the included pip and use it to install the latest pip and
    # any user-requested packages from PyPI.
    from pip._internal.cli.main import main as pip_entry_point
    args = determine_pip_install_arguments()
    sys.exit(pip_entry_point(args))


def main():
    tmpdir = None
    try:
        # Create a temporary working directory
        tmpdir = tempfile.mkdtemp()

        # Unpack the zipfile into the temporary directory
        pip_zip = os.path.join(tmpdir, "pip.zip")
        with open(pip_zip, "wb") as fp:
            fp.write(b85decode(DATA.replace(b"\n", b"")))

        # Add the zipfile to sys.path so that we can import it
        sys.path.insert(0, pip_zip)

        # Run the bootstrap
        bootstrap(tmpdir=tmpdir)
    finally:
        # Clean up our temporary working directory
        if tmpdir:
            shutil.rmtree(tmpdir, ignore_errors=True)


DATA = b"""
P)h>@6aWAK2mofX{8+Vkj=%N*003hF000jF003}la4%n9X>MtBUtcb8c|B0UYQr!Lz56RfE?c3qp%k_
SHrQn_7~2lJl@i=UNd$>)BxNOkKc^)X0-?v#)8n-qN6<M@=zzu)S>cmJxA2{mV(^18RrQA~d8sORfnv
9}yTTaLU<;$CaPPU3^2R?b=Lb<f9y9wZ2He2ID^SqVK(3-FetQzg?ZW~i=PP*o`G6RP8AkL$p^XfaAe
?4Ml<oxLIY1qQ!~sESrlexcMesdSebdnOJv6AE2HAojLa&;nbgm=qr<1MY=+d0L%bJcvCKUI$e}1y7v
&(FkNHW7#t2;Ysmb4g@=M*z4YgW~neM-nzD~vjExPg~sHs&8tO9KQH000080A{lMSa0{Q*SrA$09FG4
01p5F0B~t=FJE76VQFq(UoLQYT~bSL+b|5i`&SU@!Oq~iIS)&L9d|8u8wNv=>6nNu38Ea&`}HFgyJ@G
B9{e8sD4K$g2|O2c-|@;t@dR%;`5Qu6f^i+#IYx8|79X$VF3?d#n|xfMkA8wQAoLVDffU76;J#O)CYU
tTKs|(rtOUt}xq0efX64y=-}wYe4gv+Rewsv@!47DzwFn{pMIm#X%sAFClIW>99{f@Za2e3a^UYte1H
%y3G<XNkQ|9}&5xy4m@b>HUTlK2Lp_T}m3nsgC)$#bX09kug6MU#nM~&r24-0~c2yu2!TgU+z6-O~;x
-O@YkJ|0dA=sY-F^F})aITrzTyS?O7N5T~%P_vE*{#XPt(tDzVC+>eZ42i!91eGvPx8>ysJFuZiRYzl
Cqu4no3L)R_c2M{&P)haML0zYtRpKw0?HZ~t=E9}0<93*a^reKp2wsiXosq<ZDnF1d&EGAaqKtH_neS
PAHxCm8ml!jzxyu~m0X`+&pMkth|PEP|9MZ~c>Fv#$q{3!PIV@d3Fa6TvSqmUyJeY&DcVg-E}?LbjUB
1cn%!C6%kRp-;$05^P^$8se4pYUP)h>@6aWAK2mofX{8&kI@w?Rm00625000#L003}la4%n9aA|NYa&
>NQWpZC%E^v8$RKZT$KoGtAD+Y6@Eg2U<4^`Aul~7Q*kTeO0ilWuV9+Rc^uGwAFScre`j2$Ns(fW|Ac
W2(bdGpp`7)~~rH68&sGV^5%eytp2rf$I$P^&tDKZ^D=NXS)DphfKg^^>wjSF}!pV96<kDiP>k%L;Rl
4wR?Y1iYbW*H|QE>3jIf<PAk<Qh)HUqO__u)>GP(l7ZCQcW_>M>}!N!7zD@g@#q(H)t=BgWi%13YU$N
VmCCn}tugxz4l~bZRpUDJS?kyIdbSHLF=eD680xf+!7og$h(lpb1$A3n^FTnUH&q$TelEXHuf=@w<K}
8US-=>g^8`M}K@j9v3~Yq+HrlS^5x_C{w#E^tdu=QRK#xV=SPfwsrVmExsLP0<FczMGL>{sUSQShx9k
7)y%<bsx4!*zvn^BJ}l|xvxjwG9Gl#jYye!@43^;3o1AkE59^G)4}Q1>c5zd&U1u~C-JzmA_@Vxmg)D
)|bLpVvLV$1_gegdA{=cUb)@<^f!?@@sM!7)`e83<8bYP4FBFl%yY$tyT?t2}vUD<))vt#Y!qoK<`a_
H*MQ!GB*uJn@2f<$*0q^pqqJrUaD1E$&4J2wjG=}lYV`vbdL7DMB`GbvL1qSW%&{uL<X~~nOID3<`<K
Nm`|rmGSN0N8vcdgTO>rx^Uq4@9L!XG)xpk@qS)E`zGu>p{aY7SAvK(L8|=q|0)(qEiyW3k0!34nTp$
7FIleZUmR{O>^xexp%*qeBaL9(EF@)ruaP-CqTT3%eush)5)ZkvXbkAwe=JrsNyMfl;AJiT49i_|!qQ
iuJZ~KfbA<iHf*_$Mf6x@2MG^0hQ$$x~6SpIEUAsAZ-7*p>;u)l-|69_M)=G#MNq8Jk8gjVDjAyP6Ie
f=cOUY~IM_G=dgo$*ro75z@siJ34)S7rRVfGj<s5&7}bHq_i-P)h>@6aWAK2mofX{8-J$z%{@C0015V
000aC003}la4&FqE_8WtWn?9eu};M>3`O^T#obt*`VR~YY;QnfHmzwbC3ciJh5S8E87&>(bBYv517Wk
ANp~bsMyYmG$}2ukNeuDHNG^#ptMd*~JcpmA56q`#0W5TpB>IYnZ>tlx>JJR-$h|q#9KFT3l$ThGovM
`Z`h1@k{0zqrjTIlGh#re*%w%#go%(3HWDhs}=jz2OtQ*5LjXNW#DIpx4DusYoy!{s5eCbN6)&t+Mou
mghxP_Ew!2Ru`@Lf_lF*R=M@&`~$0|XQR000O8X0rTPQz>BIHvs?u0RjL382|tPaA|NaUukZ1WpZv|Y
%gD5X>MtBUtcb8d38~-PQyS9-R~=`vb0jUEJ#2l7?~<q*s2O$6DP5BxjWeoRsJ3)r62}wxu>V6=jZ2^
^8h*(N*&NpGAry!bPI1qDW?#fYiCKJ;y)-UvT=S?igML|#N0V|1C&T-+?m&U1H&i^Cxkl0h>f8(GeSt
y!hmM@*7^>0ZxDICF`IKwbq{?g1(QI~>zLfakj-+)%@|R<n`imIL!EOCnl4aU2kvC|v&LcG>LAL;BRs
)tPPl>FXUnWR2liI0)q792lR#k<<WI|Ni6O@Z>YOA;1gV*d3TSV!hA@Fx4{=_Su|>vITZ+Yw)Vl?|m_
=wBx}<;xHCT095Jc!zi|neZBkjkNuk%oqsf5b9u1I7=sqXI{AN)1o^8a@Yk4bqd+1TI9oO!O1FHsnE<
n%)>1#R3HP)h>@6aWAK2mofX{8&GLd6$3;006Wo000^Q003}la4%nJZggdGZeeUMVs&Y3WM5@&b}n#v
)mmF~<F*xk*RMdh4<TEUxjc0=QQN&}6Hm9cXV;rHqtP%F39VUEBm<DL6_5XW&p7}{fTX-hr!UciC4vV
B=klEk0DGSIsw>Kzt*c`p>gvF&mUWWnY+nmj$hu71qOMrpiK6<%WM0UY?QjM>E<Dd$EQ&)@i<Xu3r%y
PhA8ToTHEDZW7CZAOi<bAlPd!!3AKH77HjBNe4=k(8l4rQGWSZbg<XrIlO_8;Vrad*he|sa+jPKIy?g
mEt_b9R<`009`y#8VR`X3jU--qm?<s#jcJY?@cqmW%SxL8_->;s3#o36ok$Sh<ZD|od~Oq-&KlOwP4T
ErO_ZLu%R3ir1l-;}BWp;EL=eB?r+Ej9g*>TzIfUL?uBD0z~wRN`<_))_g$;$2iAKZqM=Wf4ozvjS#j
e%<gY(Svhy48MNDC*CFvI2ybZs)tVS{y}E9{J`fJ9eA7OX`9-7a=uTyvQ7AaC&k7ZnB&#8MJZzqqTWR
7_ph!#tk2W;#<fKd{Fkl}{P~q+w`)Y5aoJlTOUp7DhR;uJ`JqYjLiEsr=Qprm*4E+_GJFkhle?nIC4|
S`#oltk;4{M<$oYfThyw)Rv0vg^jlQM9#RAO)FIOh$Vo>`XjrmDZr3U~{uvjd>7YrPdca5JenQTSKcJ
v*v=&uUa8$$X9#<m*u8=}L3trAu6wi6ZeQ<xnvP$y+ytk{n6QgR%{m9jDgLnhaP?~4aDjTQ&(iZ)4n$
;*96nP6D|vaYxy#Sc=%NB~;lm-|A33=O<_o5G^QD?%m=4>0vT57r?uR>&rB`Rs~{Jh#$wW0{GfX{AdA
&_^l>WZHb1x{nL<tb)ean!wjp6(*Jhoa>XGps!LBvgP-@1@mEev$h63!D#TEvg=cO3z>mG@T_Z9UV?G
p#oAlWvQ7v9b9su8JE9$tvmmB7w*??rs+_Ioq?AntD2FPUSF#0&<8&)RU~&c1a2ZPL#MFw_*oaQwvhG
C2wTnRW_!_=_J4pqx;7~P=+z-H=D7KOla8uQ-W)K$=4eSSl|6eFg?&}VU(QVp54#PRJK5)Q^(ok!zf(
O(oat^xwiX&jrm|dW`($?acr4mee4<<}2G!eaLIR$HZihD|pad4HdBn%cd_G=mMWzMrY=lVVSig^k8m
|Vg|lElr)>w}H}d6JL{60CPRsHFk~R2T|42NjB%sv|SxN`{ZJ1Gk-&*7zQy-R2q+*{*BZ9tg1rGQiT$
RwDO<udE#J2S1}}yDB}VMTux520k#3!K`3X@O}%60t{Ftc-jKAb|-7}yKleN26|5hlHgl$NXz0^poCa
u^&V{r{*o?!VA<PLrY+hTGzghD(#5kNVHprZaZYt##W$uR8%mb^-?4AMW;K-FdqI4NOLJoP1w>p&1;b
`&F|mzl+0wRTY>~G*5bvt`zQRa66d2vNXoQfwBX1Gh)t4<Anc^DIX|G5f#8@K04491VI0OWQEU1z*zX
$)IX>iVN8wUs>bC9sLVg6W4O2ILD6NU3Bg;MsQ)C_Xl%%A$qPd%j7LiW&pP4JN{t#WoqD^v)6>&6l^u
`&(XOy?+-ilBrvl3L8!dNNZ)`pUd=i?WZkc;yu4_|?aYcW;vQ<&R*Ivfg2cB}&44bt5{H0s5klsH#FH
wR%y%r=l3b;v1Sm=o@?fr!Fer2uDL9L&_isoatz297jX@o{A}`XCC6WOfkP0%87KkvdJYiw3J`a_uCP
fDQ#!T$k!x23L!W)tvvTjp!Qum#K*Mk5TAh+vr~a$%H_GQrkM&H%*-&d#jq8yW|(11<rnOAC)@e}`9@
{Twzk7R0$51^Jc}CuE!GAA9Xvvbt-);$WrHdL_|lAeLBQZ_CO#8e=M(+dKloNd^Ep&_NN4$3mrXN;KY
$;k@3I`3A7~GESY1a{JrSlp+9dend4pK)TrF2-j83%<2JZo!yn?a_Np9tJ?LPX8H$W8kFZ;$7Zr{X|h
~1^}V>W;>bX?$&DFJ>=9kD<ChBIWUrr@q}LiK{Z1q{JnBo}p~-54o1LT02~gxbq^GP4#1^w?>Meol0U
3O~tMo8@*wPX&MoscP}o4<<BrMt!s~^@Vs^&T39|E6sEKM&~NHSZl4U-_r&48n#rk%gk4RS<+EeQ1*a
I<WCG1%vfp4bI#72*_G*~z5HbA>@<j_GX)MqY^ZHyqzQ+q3Px!R>4^X{0Q>+AWR-^uyvQJ_={6Lm@)^
{<P&o`+-ad;_64O0B&!=-7RGGAS7Ew^QIm8X>K6c}8M&Q(oa}gTEdn{#8KrE!M?1zvUaaV3Fa2E*dR)
FKi`Ft;+Ggx}$c=P~1dURM}nO!0tbO(Z+rLNw{=efFk{qp7qtjgCv-TZKMd3p8m!}|S)i<|W@Mic{!r
vVKne>f%5&LVZ0Ck~O(V58O@C=t$@*mbb36jVbEMJ$`LXiY;Rc@tO_s-fMd2{||QZwE5VSY4B+<0Sq#
#R5sZWW%bexDax}8S=3~m(2UdJ4<+ud#}xCji+(<q;d2>Eu{mTVIqIX5<F>K_D6&pJQdu$g6y$=$T$s
dx9$Y!j4XPWbi{gRGqw*gHQ@}h5sk-GD6pb~sS%_2br2JS3lGvCwFeqDdX60Np7C{4H-5j|G&bD5*L4
0y&&58oUwE*8cFVIn`^Zj?Jb{N5(5{*TTWVPc%cvtO+)<AYufl$xy&c4Z?4)+A>|3mXa(ELlNY48bI{
NVe$<pj-eZ4#3ki+j&$Ub>M!m$>YmKH1A`kiHiQ*43y-)7dhX|M$wzbh0!*8wWuO$+?!7}kF-)oSMbZ
k=4=^~Bzkn$82y90B{|JZ?WBo<WHOe5LjrV}0-gqxzuFGODkqO@(>E{>8t9YRMlU?`1_>o)|~urDR3w
fMFX7y>|;Q9$EoAX~ZSAkX2?Mg}F>EmDHAks;8)rup7^T<B1)3cAHj(JkVBx<1Gf04bO^wk*SqtioNn
;d`QI|p7}~*i=jsQW_%c4$662WKYGLuv!wSF%olmU4rtu*$xFJ(S)oEP`K-Y6nq7yP2(22^_H<5Alm@
Bi*V7orKH<D`o)rw1C?rK1IKs!3%*9D)u1wD8+J|Ri(6nNE@6l-Uv|2sd?4G8L%6u;SZM;9rT-y$(Xh
487(F`dtA1MmEQrMMnJReer5of(?G6PxMpNJWn$O`6S<n6`3|G8eW*EJm{3Eh#hkMH08ZG1FpEfpFs4
_REV`&=F$$`@T?0BD^{4Xez%S<^}U1Ccr$NK%=ogGP0~(ZBxF@Dq=FthX}-RiAgPMh88c@ft(#W%thN
l!9(3MjZQV3v}UlOYdmu_(oZL)W|+>Vf;*QAKdmw**zRBHE?s^C=J{(Iz_`j!?5n8{tm*mMRwrOdgVi
J^}Nt{ZD0f*x$pmpk)=6~`ybJficjO?GWYQ6geO-0#f@u4OGWpMr)@K8Z@nlgKH(`<)Q9qvqN<}#I_A
(Xl)~PeC)N4V45xc&&mwgV7MV+&DQ8Ges6&J|9y&`!)Vf)u&elX-QDSXb@Ar6>f8_7@k(YkJz8mf>->
hGK{N6=Bn%kTideQM{bsD_<EMt9R{47h0BeouDZ<=5x7IkTkUU74liW8l_R^`b&juNq&D^+Jgjgmrc>
@p2Uiv&~g^nPuUq|cm#MUlt;JmMM)-juL|@Vx}Zj=Y&Y7EKO4eaKe}XkvY%1lZ!yTUH2u=qF|-&u+%?
Ls!>HCrY%0w!koE!(tenagnyc#)}G2U?AOmz1>b*MrwW%qC%%x<lii}(|S2tA)@IK&5B?ao@5RTw>Id
;J%I}+j3Jscf>l{mcPN(u1bihp_PpW|(nUn)g~VfP*%|rX*0QzuwxW~Z!~};w!&;L@ND9pHYwPSJG)u
@j^?ibQ+iF9eH386hbDS{saG_)8a~yy&GEufTLpFY+wX>^%<vH@FZrSkw$V;v-u9FWpFE8J`e0O!ZPF
}Cy-$46J_ilbLoDcLT<mTUK{JnQET%SK;(RlLcfLjx|%8mY&WE#UL{4~C@`fz}TA2v`jTkSpf65qZa(
*jI6XlYjZdrIKgWaT`C<LK6RdzbZ9Grr&R#{)rs<M$G}o2YK+oIRrL93>^X;Y0k6Xa24WKKze~-*E;w
A^)Qt^|%UT5Q-K4H_C6(_K)3?i?om&#@dTRQ_{LTUkgzSKUn-1P)h>@6aWAK2mofX{8&Jz&khR=004m
~000&M003}la4%nJZggdGZeeUMV_{=xWiD`e-CAvr+r|<8u3xcLV1z1UUSc?ID?mjZ=N!B6OAtHohr@
wbi7RP+6v=RxCo4t&d!LzIl1q`gT$-j0Dj2f3FSGML&n#~`oj#N6of5BQF1Kp0ayyw$r;~}^mqlg8PM
Te&SIy%`Q{>I>tk`aKzHJ^0Guc$dUX;?(4&jHt!=sz9#}dn%@u&H5F22!gI~T9C!S~zJ>LQof#FNowo
ZPBBEvmSb>l;aD#a3=jL*c#L&V|mcs>({?JIUo<^+#@1WkB>UinY~QOL8sqBG+q~>7Nvn3z=cUU@%sn
){2>J_r1(-u_yhoQ!0C|GsRm+cJ7N*WhPE_rPem7tE?gL4Uha#Wq0h#bbiyUe}&(7EIkk-&06MaY%z-
-TeU9}aMY?5&yJm<f{ADvv&oIlQ*)jQWNEcQ9+23A<eN;$OH?J6jl0BKWnb}Fl(34EWHy<+{r=^*FW)
48fA{uH^5*I5ORS$3mBxmcTn_#?N!3Oq<c?r=ZKHI--g9MaH5d50o{5Klr5}rlzz073y|Q(c3yDFw%9
JoW`RLJOQEV_oB*@#UV@%#oI}FaGv*NVgmnKR<6~ZJp>S&hls~VnVR4FS7wU}izoloatx|q)9Lgl8eR
3gn<YhF2HdX+og2T<%zk4&ucHH;KZdHr-Yi+Ac%s<+D62#T1jGii+Am~16^3Mp0)O|IdhJpWLXRdK6R
W#F?EzNxpE#>l3qL@KQmY%OvdGhtE-;(zaUkjWR~J+@XwVM!|%zj-Qd&UL$3@vyhHNfH^AZRQ~bu*I5
xQ{<juR%Ttoz_YmBH*2TBzJinFh3&`)a9o&}94FQWvPSJxw~>yHyDiK9b~-=c7haaQdG<yKZjEQ26td
t5V#X=^kQZHd+(Yzl75OnXk!I)z)FZ9f*T#yKYMK35=v<}ZpzW?>r_~&NJ`*35ILI6X3b9qWf(I!fb3
xIMq1xaHr_`0VBphxo4zOsEe{P$d0lAOFLZxUQS?q`JUxA^uq-PBV^>#;D`xZQ68c~e^Mr7u^cvHzOr
}&PX%+v0)wXDF+s;Eia!gx=h54dtlgx>!#1@F@ZE0O{~A@Q*%X~_Sx-KIBg6~`?_yU>PBPv+vY+v#wo
Gez(0t3Iu3$|}vs;7C)inxHtgoSh>)4OdTF!lN`o+rG@#S)Hn|=m=Ma_VOdVk|f;g9KU=iB1^P(4hX>
$)<vnDC+RGExKd=qRG1Y0X`J`1YMrH=y*3+Fffd1tJ|L5-5(SRRY~d_k9$}iiJsm>`7lYJP#^sSzzEZ
Ths&nj^pZJAy3YV~$T66GPu^h!7L7-PU)AlH+G{*sfowcP|TwH7+QN4<>_@X?P@&eW4LK{;nbMdD~e|
a+Wu&e25QD=jk4hAXZ%vLY-V7DKqblb6e>7=AM1UZgQwuQ^v6p^22nQ&3ZYHLFd-Y1OS>r7SwJ)_ojM
S4M^MlQ6Jm|<ih_tld*Olci`l&2l)4E)9xR%T$pmY9p6|Ij^lwGo*@=4ZNU7K<0fLEX}}o?VPL+Fsru
zEE^2wTBMUS&+&EiA!RvCBBd@f{3S}g8wbUqT4EZb|%5)C}W<Zt{#~JagRx;|CXE<j!ix%F_v@TDawF
ahDBL#|A82zB;}GD`)bW43-Q@o33_x`K<)XvPNF7%T{+RN7LTsyUd*dUi^tu=<HeKi;mP9qx|7ydbtW
|^H;6pcT{SE;^A1@i4thFx*_BVOLcqj96~dMT3DK1?uuaMFqz1x*u8xioZ)S;&Fgy0>_7kF)?kW(N${
Y^ogGov*r*NHw$VT)v3yF7C9Q;M}b2ffN)T(RFXUy0i+d;}N1z}!eTSC{TR%rMn6AXD9t@bTIq)!ME+
dR)viXR>frCkLj2DvOWkdaxD8lm&1urK#z#{H8@FRQAkn)KqCi+VVw%d~-$1Ue60q-l&8q;!h_u?TIe
G@;D9a2|x7$S?6;1>!?-4P^%ECLpQ|#Uu+Nqp43+bLI{~97w*(@54aAC6Jsi;NcnfQ;i3@?=;PEi^7;
U;_q1peSNh=uyd_*=yp?s9r6)C`wZR3e-^6-*z>>OUV&H~sqOZ!eTlK0{s@`94j0S(C<sI`Kw!k^TY~
VkmKfm+RwSsw%=w%PJRYcwqk+jh!0q@v&|Fp&H<YXEGDu5AW~VKxeLIK}P~_Q>ETR}IV-v*;j&0itax
Od^9Xc&D2&btpYnt?iR$lK{7^42m@zlZ7BDWH7it<B8mdmI=(XX#MFQp7v=laK5#o{vF#v;D(;T2-#w
D<{a9C=yeQ*@-Ok-CG+q_YNuHINE>zKFkw<CrEPBDkd`mKS>)OJ_Jn5nWjaQiEbqe@Vk6kD;vXdUvXn
USZHfU7=nR&R8i7s}!-C2HN+1o%2O%={UH3OUM4ff*f{wy>sy80EpSBk6mg!f}4uT*?+vJ>Q?~Y-1W;
;P>$cR=X)<E!}-R9d(hzqpXbAFE9%om6Yi*?9sgqpO@2RVx5EX5J%Z8-^OAS=jvcF&{j_kV*e{2dS5d
g2vypQJ=*(Z3x!-&Pl=m#%!kO$22y;^2ZFTGq(8sy-(%nQw-PyC=N_VX`dY3jNNvS~RwdzecaC4#rJ}
&0t#2=RDfY{&wcW)J^YE^He!7P2IFSlsyD0ah4E*`k_jQ<d?D5lf#&1s=rzq^-~qf$WuC2}taQN&gnE
du2iw(bMexcMldz>=f$S<l78PbmLz#q8cHCn21Y+t`TuQ8F8<_cQS|CrPekK||~M)eBjzcNfa8@5e;v
s<AAo0UjD`+=M;0QT|i)DcMtw>9hauX}*oCpHuE^kP<q9?vW6Z`I&HD($zzUvrTuZr$c!v3T|toUZU;
z59rTk9d^4cfh7Xyc8cXf6n8r3D)qWjoENqI9L4vL^KElcNx+Z(wdV0W!W%<$oW$CT?PdQ?yYC8guf6
PDa>tk7y|{dxe0Xtr`6_w#^x2Ecz5%ycu>wLkCVPHmlDgaBc1d8(0kZ5f#=1Va^S#X54BC_Qmy|IACd
Sfjmsk}=<_pt_dKe-s`^_OwblWlAJ@gm3yZN9<wl6T~vW4$roAqvK(!KLYd`n4hhN702c!ONeQ#0s=b
HRl;eJ#-IG)L*iu6K#<Q<efrz)mYcOxNZKy$Tpl8fOlMD<fT~Pd4HUGt`CUw6>dvf1VCg>1g4*Y+fr-
;W%HB4zkKY{O4+tc4gGZks`P9oD0%)P^O{>W_G5yjEj1{(6ABDXT;Gm)42cn9`HjY%R#nbcs<A}+;K=
jh#E5Tm<z}EgnIqPEGrI9`fVlGYEvVa5p8%tnuPx60VG#+s;}&<N~XrW5jtmJU8!9@ZmzF4MNNHxgSC
eF3%5i0m9f9Y8<ul#OcIy8n_Hwo!+mxii{9=#P4>UCH}(~1z~R|Drrv3ewO@5+Al<#r{9QB>WGNTQ!H
rxn?2&p8*_|BJyR8c;!heUaUP8ceG8XKOJ3!J{C}iq?p}BTzS5>di+=O*2nj86_zZ*klY>AQ9Vs5*`T
ni+DE`!01>%*DGL7IMs7%8yGOYEGgl3Dmd)-xX30V%%i&QF4<Umr-K<**e9)xA955A+qj>_3LcCvYv#
ozIF{&yfQ!>XaY39rHjX{%!g>iBCfK|3c#DGBYP4)28n2_TP*}ky`H+`lPfCIn?K(N|O{AIxB!fT;Y!
TRb(#Od7W>HMF)9C>WeS^Ay(@u#r>e!FU4bbLa~tM9Z>7HLsrj<I!oEKbo?onYG3QR=qF4SpKJX;(B+
%7)CTZNv*K1&hf32+4|}f755)fk*s8Yxjy2YYzkmD9+XcS_?9{G)tTjB-zhTZtcHQ-Mw*;WN`0|Udo;
;>tKpxxDZRIJA)=%h92<T>}=bSV+<d#17F&2HMZ=Hqc4<v>LdO#Pvy&IV3c-}B>IVStS#12j3U#4#qu
%o0ui4v=NEBH3Uor8d^YUg$Qy8E0vFj01i&<~nhZ6$Jb5U>RZoN*2MbecTBrn@seyJTR3@ujn|ED<y7
E-d?WY~ezf|5oa>HToA&O9KQH000080A{lMShx=DdDIX90Jb&&03HAU0B~t=FJEbHbY*gGVQepBZ*FF
3XLWL6bZKvHE^v9xTWxRK$PxaoU$MvF5D6zUO<NQ_0cz_zJ2~SVJFt`76^6j0#g)Z|A_*>KM>X8v-e+
ca$z77NeL+9e2x5ucot^i$9S1@1W09}Yn{5@>X_1RfoX0nEBlB7)S#QhH=(5;IQOjzR=0#TA>}I0_k;
fZ365>#ayDF_~nTs?RO9muXX(m;OMYnObrB$Ekw}_Q0mT6qeMBJtITErU2f%q(USagOjfUvnvbGss~U
n(H6WW2`aLrA+O482O@ye2G!O7ojcio2ppL?YF)N&)6Z+^uB=)YsCWW@*HU2aKF3<Fpb>I(k(Vn^6!1
qfxpki>fwT%D7Upvd^+&8E4XdE0q1Dc4|ZbM7=BNVDtDe-%Z6)x~!+-1PqL?GdUHfslxX&dG}#g;_G=
yD8<=SeAt$Nt>Khu8AfT2O?VZ`FH6bGl!ZJ7*+O`dJFcptn)aW+fjE9Fwpnsk)IZ46B2Hv79ZiPL+16
>+91)jgl2&T(x)8!D<JvC&<>c(>{Flr9%b_|q4sUK`eTpaG?cN=mR4wgtnX7FjBVaVe=j~=Rx`^*Io$
pyhV(v*S?7kK+#N`^0)^VPUeopfQ8;lUf0eugqLe<q|H2U%U?9IvB=!e70<Fmte$5<B-c4?jlB3)TRh
0K)HZ|K}$bbR(HqV<>2$=kE@i{m5Ocq=Of831;$mRSkydLceQA3x(jC5n}=n2K~28XH$K9O)%<rdEsl
<K^+iJlKL7zym!WiLT31F4I-I<P~pE&wn^Pod-8raUExR)#XmrawC386Ul2XPd*&a1C`cNzrXsFR`oW
{7UDR+O{*ej+xNhNw0R)&TfKqh_5S32WEl14<n-7si#{D*@KV@U<t%qWe<H($DJUr6`KRNHi<6_{==|
d7_yW{2)uE<iYQ7QO_A_B`KjS>-BON{Zba;Al6rG+Q9!2M8r~hmKx*&Yu1aLIUSQW9nQOj`@k*A3wXa
t0IcK+dbCf>!nYbhWBb}9wi<QEawH5|^i#?wONMYV~u^xu-a3_*Y^Oyo*L%?pM*rvGNFapK@_^n1oUg
a>*Tf0o8Ol6olk3u0R(Z{jKe+gNW@v8|R;jHScaqGI1WAumR-7{Z)?!TRn%(<H29nZ-+}d_+2V5KMR_
)S6eRI<9I(&UYLf;HAc?1MBLKvjqvZ$g`a&E4c#WvI3S3ekk5hA#hZ=_U|K2eUd5!0J(wOBQT~zKKaB
ed|AvaIzbqKl{JMGUfLic$<0Mzt3sFpM&srUv+rlQ6G<TzZwB}37!Z<zf*BkGM;{we;0Q=Yp$I$>tKh
w?)^VxCuGoq@gc$6BU`gsPwPA(#gww-IU<cX6$=_QDljc(ur`XYV(PNK-Nta=vDzmg6gZ`;_Ju&QqRz
{wuh&afOnRygouE>K;TRs{_YIMz3y$3A2YH%!62p7H%|5c><m_AKK$NNph3Tj2KNE9X}gycOeRC+KbK
WKDmG2&nD5;_>?dZ!^|hNL{{m;RXyAcMXycaMSSks-g75GpyyaqypDGHn(xdVS{|(&Khj2Mzr~Ba_R!
$1t&cp`#tX7`E&o&<Op$Ip1|pvmx0{J4?xT&BRrg)r;;r@_ty?=jgOcnA!ROy<285SYLk|7xfd^OuFP
Gi``fjYBhLY6}N~y3f3k#yszMW$eiNk5*9!S0ofq~qAz};W>QIp^kJPUp^?HO1lC%?`?Syx-=DxMBO$
5bKa~h<zDUU)8CC#qv&(c0#52X`s=BBohh3em_OjFzi4cIbK(=`Te}@fP%Z)Fwrv)yuaR#re*nnbSE<
F}-ZVHp4qpu5`L?2w&WRI{%Q&vFk7AkfN?8q8(A!D^8ZfZf$Q5#`^4sep;8Q3C;>sZqdV1%qf@Jg4+J
dBVvCG5SCnWc3UAqUS^Q>-pB;?N9;7f4()<dhLbgISZ!vOii-idE#2y%c?Dy|~(z9F7{ulTq^yX4*g`
%*d0|ZpOTQW1>SR;?F!^zSjqPtC-%m3=T?=CPo!VZtZagLaix_7DxaH8R+}{Ll6?j<GK%zVIsn6|FDV
6F(NN=*ABXqNpGkBr2R&`4=wA#S^Lpn&>}o<k#BkXLi`|?F@>@_N>F4e>MCA-CTeuCgvU4FM57>F7I`
N`I>A=6Uf|&ZhQiNObh7Wof^^~Dqs-KA@JkD3wfRmm^|Qie*Fy&pt>GRX{E;z0?e*B9_YYrr=%z@J7t
5q&!;`dA$X&G7L}Fn}8n6qP9aU(mYrT|14;VC?gp&f=%&$e4b-;}w<B4l%IcG+WV)^#tz;I59z%^wp)
}|)}JgSRGCdghI>KcF0CU=I+3yyx;^>RpMce_q+)>75*b7@hf^{#Cz7`j~wDWR<DuHHKy1NL_&b@m3U
Rl20X_gJ5(9}~ieJV9$Db+zlb5gn;DH;7m*dm@+BVK<&!{bA9js9dg#6GVzH>~0335rQoX5yCgB<(q9
6xO&AJJ;+19pP@vSqJl_Z3ZVu&5#)RjIdY<uS)OqppaJIb*gay@!CLcxV3S;{ojt)<21dq23n14f`k=
w1;H^Y_wf>eHDBZ{vx=27LZm4{qx{kX>`bR(MR#<pCd8SNTdakgmCrK0)19E&J+M<Tp3gl2Y!YIWCQI
!gY)i%=wi?9U?^&gNMZ^~@f0T!GU2#d=#Q4=&lJmy+6)*hMYOjZ7}wy!zfFN+Pre-i3))Pve9yF8vS8
}>!Wm5UFe-@WDiL*NKo?Gg4=%XCHpA9i!^*l-%*4<#+0=$|2DElblWTF19CYP^D*Uktj9=Ix5$PDN>(
N{<=6m$R51j{E8QQr5AlEv1KL(@_e;C1Q<%Z_~G7i#50q2Br_Tj#Xriwk_0&j~M-!#c`7K7LNwjLF{9
X9wToDe>X&5`Mh4Rk%0xaLG13>#MS2rINLZo_5|Xn-ZtN-e8UR&k=8$7-@e|}{7=*nLZqWilKU7lpPB
JKZO{J)+CQMi{nYvq#b)a;?<=_}z<cc#eQoWe*nM-*O<KKG+{KzG4KN9NtDj$G&`<CNd3A>DK=-;$e7
H)J`Rhd}-lI$eFvM%_!Ba4~-rj^k4^+=pd~oW=O}yjOW>X@CidVI+SY3h!iSa#$O-Y{c8HUe~x{cpq+
Vqpi>}mhu1R>biBMJ2-UTb6DR+Z#r|6l{8s~wyLa^A3?H9u**R6F>#(pYJ)K=3%B8_i*wuZnT-OO@(`
tPtNSREsOEoE^a)GcrgvDzKKYmS0eDC|`8#{m9sMrtq1alZN^v*q2I_bjhda!eX4ac{APcNlHe2nf5X
&`r#zLC}nPC8{7pGQsY&Bt)oMH#CYW&V3M!%OEx9~BKt`g{ro=rTLp)?F}h;ODv_Y}<qD(~$8ZBh^vz
I1yk}}3P*yVFhrQ<dLjNz`SLrQOPgKPgN1D#e3#a2Utbu!!JY5YGL46;*mrq<Jab09;q@`ORX@3vKgh
4AHqsNJacY-3PS;neTRG<0cmDJ!{)s)wS6Wy<QNE(*>qpYAXRlRG8Z`1LXV!yKY4E#{E8}?N?k3@QVx
pQQJq*PeLG}spw<yLoGjC0iBLUCD42__YfRNyKHoc^&8a?M-nuCykL>H~QQwI?2Yr?R&p(W_o=>7KMq
fZN#fl?KAXF?dt!=uM82^_v6#o3@0@-Ok+uNlN1ji?2GJ39mKbzPf5|`4(4yn7u~sI2Tv&bBVmow^_C
r^s!nu`<=ea&uPiG^hExip0h}{tp0sN4xB~^TxRDU6h=T0Thx32ldcdUmO=SX4H`}RL-WB_+djQbFrw
wWZYZNUS?SwlnyIi>ZncdvW9<E{vCZFfS66sBX$y-h(gxMsGz<%Zulo7XpnLMVx)zUb=AD(pQNwpWjX
c?Bz5G_a6yv7P_pO@Pz&f?Z^n0%KLzjhVzLlfi+fFvj$kAEjR#*dpTXX7XDNEfPFm2YhlvC6pNP2s`C
TnBOVO%1rCgV=dH0fG1<E6`?h6lPey7I4FJ6+0I*R$Ws>bg*J9K3P75;1oQ?+$N|@ZT5^Jr1U#%Z@$#
qdV=o+AeKPG467Y^x0;z(8{Lf<R?AtXOjT%!K`&43+=c`--kAJT|z~PYRd)&JL&sWGauASp+}t-#&fy
f@anN)7N>{X+O;++UE=Axy`-R4(KVYT@YS+P@nl<zCBE0Pxn$Cynij+EF5XSa|E-Ixy)6ozrALL1uQ)
VSw$*jFmU){l=nJ;^)|#f8ws#DSngh<Jn+^Anix}G7n9yGIQU+`kr|bM_L<{-TvS51W=1GVmRu3y6;j
?eYZxFeklh-!2PTW*27RJ1D;$RZ{F;DSU9!dItpqHq*a4Dr&*LA68uU_3Ch1y=zkkzYlSH`c(w0wo!d
@I$fKY#z1KRqW29-90b&WS;nD)RX%FcTB1xeB}QQ1>8~>lnTa!CN_3=k5>lXRf(4kOvQN$J6zvvi;|?
>95~^J)8LOIsZR-(&mRRNWLPMa;JH2?U+=*JT)%N8+~dV*?`OIdbMDNgJw1%r|yn9*xc;26ua@I3&lf
fYCX1T|FXZF?Z3z1%}*uvXZA#8ynM$)IB7pu94&@?!ymTZn(yOHu|*E6oebp>Eu?KrnsROC0w{UkKoR
t<ydHM7IxsMXbugGiLX91PhAw5zX9s022JCZ+flXtTqM&A|CtTf&w2|^Vo|*b?aL~-Ry7o+`5!+Src9
DOz<7vvH_f^gulA+q(SH*yoV?zxh^(-(F3Wrson853IdPs;9ZI^MxAYk9{2cf}07*3LPL)DvbV~_)lE
z_dJ@~c137It)QD6Qp{rbpYG{~XR;cd0~3ZA5F@0^-+Sf1PP9#XrQj<yy~pkp9)OY4@0`!fH>|))7N@
D9o3}KM9kzMklo&ykhQ6#B}Yd9gL_st4Q<(q&8U?iEF5#?yOb`9H<4twn#&Jl&-|96%-l<8uN@W03Z{
s(gZP^_R_#HyUw~Qvdl@JuXmk-ITSxZaJSt0#1<Y3H2ZY5Qkg-X9a($ZdrVcC#XFsj&^nsw3c=ZzJZ^
Li_U@45s2cI<rpTeNsH3pd>}%lQ(ELVO5t0irCnB=#88z^m5|{6ePfus!U2)rtu<K?6ShB5kDFM1x+n
jmZ$^>T6pH;KA0hVgTcZya70v^-ZSF`V(K5Wm_TJ6u*4ixbE)xw=eDP?s)EVh3=U`j*Nwc(7iOOVd~+
VI2br-QIFfJf7+-RTBa^8T$t_W)YeNi{o5+z9FTgFUEp?~Ta>^e~?LHxop9tL&uE9G~Q!yU2s&a$Qe2
5Ad8`cpSgg^WLDyEFYAj9<&~SM=uuM-A|W&doO`p_&mIQ)!FLYydy7vYV*R6OnkAYqBJ)UhsxlmG7g$
Y&~SulBl4h~D}lX35uL))$(#o7&l;!w$mr0_5!;c}e}hA#gDGk}Q>@YO9|LTbK7O%idk^zYqoH%f;>x
$Z6H<LmZv8(kTXUO&l>(Z)V<*U6Ve-8d-85u7zd`gnM)dYxoc-~+7iSaK4nCSO{@%<{xA64Resy*5dh
r!eyMO!DZ4B6^&aA5j14RT+TUnJN{h>+t&UKn2!TxgZV)^katKl`aA=LxzmJAVf<IUWt|91`!Usu7sJ
|g1j-Y5#~pI$tS@4NFk-&7BiVDw*5O9KQH000080A{lMSP)*zh&mkr02^Zf02=@R0B~t=FJEbHbY*gG
VQepDcw=R7bZKvHb1ras-97Dc<H&LU^%P@lQcIpmT<&aNxs>S2IxY8Bb^D=6+Ou6c1p<K~2@3>h3?MC
!#i~@E!Ku7P-XU+|CrN+I3<e*hsPk2&9MySA0y8~5Jw5$BW6$#@pCY*`lRQ(RQZg3hqR6ZHBCkrZ3Zw
gQF8!mU>qVl(GLNfNigzEcuEqNg*P<-eqRd6IT;)Y6W<|afVYV(8Nj4Xc34V&ZRkHGfBr9c+h3OqMKg
w6K2utY;f(if0Pb(RfIC3tgQiBVpFp>fJd6=eRmZVY{xaC3~scNbbgf{UAo>gij6kwjlBFjq=%azPxk
yG=ff8=@I(UHbB%ClKAUxkH|h4ZYGpUO0unkQ)<g{iE6&F3&T^K%uJ3#V;i+o`oWBGeO@cA4j?GBk=7
VUmr+94Ne+u1C;kCBu>%m+KW0PPe@N<HaO6dowxv?)?3?Bk?MU%8@uPk#u=65^ob#;=lMH9f=RLfcWi
W249XCBGLW<NRStPkwgn0CaCh%kXW4Y&yo4UP=JP)&_@=RQdMcW1Jp7s?yHr7Bvlly<c_9DQ#&pA4r?
%L&hPk0z#sKqgbImj+6Qmo_fh@20bKsMlB!fb@TIJ2e94b-7HS34k?rn=8~vp$!#FHM)AO59$yY$wBA
Hf5iCz6*VEi9EP$hDv?taccar~r^OPRq;k!55dP7Lq(b6LKnXM-Tf!lev?;nC62i=!9fDhg+_JdKgVU
L3`8CW1r-_i`Feg9tDisAB=R4aN9tF$Jb#q7|~NiVQwrMapO~D7=5W3CBO){&Fzp&*5kP;K8mK;!eX&
@jlOhA`E|3$XW6!z&!<%i2>sQ0fmu>k8W_eMmXy2h+b$0I<~AsPe0=ihDJ#80|u!d5Z(xn@dg%16cI3
sU}__JHRN~rM@(}f6g_~|m7P}_7gz~o)&K?>sNs=Il%5uh<4EKWvY4g$<B6Bdv%HYrQ2es5y&ZJs{g7
>VLR+t=KQ$csf69|=fC&0(l_uo?_#uA`rfHbnpIjG}9O7z6X{eOANLG`g$cup$z<T;1rmh!KOkvHD@r
1-yJ_#?~^;HtWsH#jN3&eb>VVq{%69r>f;_4_sUWwRth6S4C1@KLRA~HuQi7KG*nTjNzQ6_@SQX&-7D
vK5(pCK<N(Fl9UjN~-HF3YtUg5g2Cyeb$40=JY(fvi@(n1ld_UI^F@2)fD=*tD>2GYQ0xWTQ<KW+F@#
D4Hxvt5_1WFpd+Jc}8rH01l{z5|zQ{&@DuEmts5?j|&h(A}plA5OfXlJZTX^4Q8kZ(^$e-000>R<N@>
m9$u%?B@Fxr!efQ7SbPKV7zAj}RmD9>po11vE5Pj27}by*Ppc#a{<`zcN*Sirlcx>C&uEvz)=bJEsCi
MzbT+cTKC8dp1A`umms%~{c!UpdtM?cd8Q|jGzJ!fq9@}ot$VQRe;GT!JC@t!Snm9%};J&7Pds{cri{
U_Ow{;rha=|uR9@re$^U3BNq+t>6_f3oh6aK6v%nLEeR0aGJ0>_}eQj-YR9iBZTv5bA&0i;=@MH3wHt
AdSHqIwHUlvKEc!n2*c;YhEG0|>>n8S58b16<wcgxJBi4~|+Rwv>o%*Eis@QYD&T)P9WZf1#Pvu$_-A
24mt!^M#91jZCwR*<2@vlbWwJ@33qy$x>*%x9blr?Du99%Tdt8es6(6hCq!BAI_T!mU%Gr?QWZS|FWU
xK|n$`2z;Zlx5r}Bob&c;Z|Lq=u<HtdfsKg0fa#8%?MB*Z&{)uY!wtMvQ#<ZS3y)tETUgdsYfWq2R{!
d4smZQe>R-JrE%|j@`@6TbT?yUV{)X1gw%+jT`azSVAj1Q#p?3?zegg&nayD*{+s1A!16-^3*nya$9y
`I!8hg0Yoqb@1DVZq3TT9gU&YoE(5}c8lce7zQTQJ?y_;zDqY;QilJr+04)0(N^mDhsgIj{j0ln{Die
yE}(3GysmHzm&talu-TR1~Q?%>yIWf`v@wLzr3rN84?#eAB}<cBx}eHV3S+-DzO9|6I--^|pxG>*@aS
FeeU~Z~y1NfO^8~Z_lVS+W+-0|FNUP@MoEvF;ae($^G>||NF0h`S-7%H$!-O&<vZ#_TMt+zj;Bu8`yI
PEu|;+PpmsBo{)>@-^%Ttx8sEisIh%pTFn_lfL?AXw4E6AN`~E_`#K-Au1%0#YVTZ8yP8X&GWZ890}&
Dlzn+DwR~7$S4Thb09!#Xe=V?LylzB#La9L=Q2<9hFvNKDvTb|~E?!%e)mTcgS1+(>Z(BU*HD{!I6by
V<#{mU~7j#UMDa=ZM?Z)JvFhLFa6MNcPkd%7;G4vst%Vq6vMLe-sJpzji;;Qht=qR9Uwqw*W{taSWE4
Z2=(J=A5GV65|TAv3XBueiHk=F1dKba6*M+E}f@`CHzN!1XPG?9Im%f5L(8{H_m&_QH~}8(a8exBJ+1
_j+7Cb`L%qnFwqh`DreE$7*e?zA^k}-Wl+t_9h~DC^j6h8))#uZHxPiA&4$jcY}E30Grq=(ksNpe+bh
gZc`JZw*C)US2R+L<Hn`Pt>CCHMw*#)+G5FK40^7`ouxQ<C~Ln7bJ(0gZJ>JAT?ZtUs-*S(?G!Lp2do
7Q5l-_5u#1RR$;xk$rM6><Fy57v;$m_ke)Gj|#SA1i!i;4Z!kj_suVj?Wl8Ct0_Z<9&&aNP${k#n9EX
MN~R`>eZ7#8E(p~|zrBktWnFyuEBZ(TN?c}?mAuWxwP+y4jriR<-FN6B|dZI=_n2p0%<ZYbPH`b#Cec
a!VWSEtvf9@;kE#dqJ1&)>iP;JGn1mCQ3hN$MrB;kRf#V)!@#7p?#_lcmB?<RW}v3yx%liR`2J5d-#=
fE^K4ad-C`p1#k^*Lju2G@H9S(lIiOhb-(94m=~BLsF6HT99ypkzl#w3gbK_heu&?bTVrht}%QPSKLk
(B*%0jfgDBE3i=%q;EQ3xU_i996VBS3=~BSJ3BdR4InS{Wj#pt3E;anqCSmg_v2?p_Yb2E6_zk1I4Z2
SyF#)lIj2lckz<4fDX%|Bb{a$3rc0p7@QsGBCvgF`J@g?WCOKO<n&cMtI@e$brp(8&yAzc%=n#w4w6f
ZpzE1TOL<UrAJYD}0G(hahYM4H@7g8Lu~<O~c}Q<jl7VLL=L^T-$2bf>s=SRA>Sws-6-pt1Jw*|xTrV
1k8fifIKj=$L0t9zl%9m=zE<-KB(1y-7;0!g9*&At~|<<rGOTOdeAom6XzNar?d{&=dC%PtJhEAb=xM
|JwA`a!bZuTa8{t7+*ijm(wJpne3d_(}+yv3>Ocy;z)R$*1>#GI3!Ak$R0%Bu$Zfx<M9`_!|vjN-Xer
$DK-pmOY6O<dqT%8$cniHo+#V|PrZ^xQ0-fzh74}-0cKAS3D|JVC?J>=fKW3KXricdm9Aawq%alA$_q
@Bv;038iMcW6IVTcDRe@T!(AvQnS+SG`zeF~&T;BkPeb3wEGzFa+ul3+EenJhAC<4PtRI72Bk71kC8x
AB@Xca4JT?S2H5(B@9M;HT7p&9zbu&@VERlsHt#3K>+GK@>~cL8gthbUHL52=j=rYJdE)PIbW6TnUtQ
PUmaqL2?sUMaFGUnRxCL%md#`{3T>)ul;P;?j|URPRc6wD+=n%!_;Q9y55k$I*LpeSLvIbu*sPvveZ$
2$pK@Xgl6}obz`QKAx!q@VdDnEytRz>5=zjlE_s~=YVViBIrlCg9vQXu?Hhjy&zxQ8Eo(BC^e~FwMPY
-K9pwB1rDtSGz7h;Z_U@1a?rqjcVi7ri@7<bTSMTs!r8E>s}bllFu5-Sjq+bi>{@sZkNbu<GiqSd8K~
n=*!hh_J*e(Ae5OiLI%`)Gu;a%4ej#Ow@)9-lK1r$D<9?IuB4dw+(D|6bY_P0EGT43KoVE<I0m((~5T
pjupZl;oi=tYULl<C8uZGuW%opwRSsT<@N)9~fc2o`1GMYHH$hO;aOg5`)X?o)2#sb>D<WbORDoyB15
4%N1)-Ip#gp;&MbzXZO<vxm`R4r>m%$7<xo=fSPf35O?qOGwyfB->YRlOoa9o$D+lMS`E1G9^B+I>_3
M4;Tl4kN|EgUP1|*HkPhvZf99v7AGrZH(NMf`J8|(hE7CpMZBnn2boRW!4aMbU0ymxNjq%+n>Rw>6T1
^xi!O}rDmpC03++~OZ$D7NTx+b(7;9b(R@L0;SGJZULk0Fg`X|YLcgNVXR>8G#d~SZ=8Z*lOCg8`%WP
_Nx5u4isx6n?)TmR|75!GrLkM(JPoR-#9rkeilWxE}TP){nojp=v-wKlm-5C|yyNGQ3Xw~&>DY0(>So
#?P8vlvL+4je=ud1mINwJ~Rjn|F3ac|eLQWgN1=~&`Qk(nLQxw`RKegd~D9-~b$X4~l}l?!S6F#uOJD
w0(#!)r4O1`47)27#VrPAY^;oB}jFm18_%RVo$O-0rlRl3Am3f3b{i0n=TsQ0>>zEQ)`T3&w4HZ(okD
4W}CnM94l$!+;A~2Q$t&-fTcB4qQx!TfrFTW(K!6pWptFdENZ*FEzs2Z)`x>)w+SiB_r{}4V5pu<F!T
`?kQmD4W@P}027`UQf9X%s@lU9Lo7uAo1cxmq5^BEqR`H)O4D_3cpv3df+YpWI~&VK`-7q;aNAh7T_M
h<C69k~Om$b(S39FcGRFu3EGAc&I~#E%w8w^#8c>-O0qlwUdeDBF$|W226pP(8vtg_LsE5E*^3-|Sl6
;1SDE-X$XG_4%E)=$cr3z1I(;RZ!HIg`4hdp1D)EexOjJw5PGhwDdkLMQlm__1GlW*F~4>;tl_6J6J|
LmOvk@krV=1oA8S6C?yq-1t`Twr*^%n4lRI;_w0ZHMvAHfW|f%ru6(HbhH6>gH|WKYQZgxsH@wW>GJ*
u*<Bu49osGDZSSwsnRl80dZ|}VM@xuyv{L_gL*3$7)6~?sUx~cSP8q+a@l2(aQOb1PF~!2c0h^~+}zf
{!WAAm(MFIqbe!h<!TY*5{W_Sitd|IlK9~xoJh+$ZlQdjT<4}M=mVREuvZ$2_5+_QP##jaUEQs((MP|
;bIKD5mav|A*#g^+%SeXd{Fn@vRm7XTR>NID6n#bz_2Uw{9yMari>VplB1}wu}pp01UvcBzbUt`_z9E
D5P`do$61s}T8A9lHPACuDODRDTK6azPc1D8<v)gE7(qq|p%`z(LV#`8R<V97!%#`QRQ2vKXniXDqn^
uJ1>n2)KQQ!qhz0W(b3psr`LB!V3Re&5WQQ-o(1)?$$6j~HW@429SML|lCe0K7`6vX>>yA47tmDrJd7
T2LSoFwCE=k_;t;o{VCLcEPFDSV}CPCh?+l`s4evD+_~<Xn_Jq@HNmTmf&rn9P-5}*8JZC0He2g_Yzl
z4ulf(Y*|7l8i+`~Lp5YNOl~P1YQ*0-W1TNqrQur3%vFxgS3;>iP>yTI2(}00D9r^D)0RIUCpZYXI+z
RVdOPf(mtb+sNhOrl46z5`9DQX|Dl?cA=b!588l{CB;0Vn|PBQ8xh2<<9JV_RD%JKoYj`Ef=EWo8VM>
`x3<IisJv&UOAaZqZG)I&|pOszQ*+3`e-zo<7BZRCDgg~4XtR%msB6;dF3f}&}xNQITSG=IHber-b$)
nJqmSR0RCrGzJ|5rx0;AWD+axf0jJ;uK{~BwiBa1t*T-jH5H2Pp&Oi=;!y1rRBofhIqn^Ar)}xd;_rC
s!Az51$z}|T1b_rur*;Z1M?D{hI=sTk6ik7jXM0HtH+(WP@-@!+&(w?W{gB6{q~29f3R$B!0HV3^on=
aqY*@E?UkiGaM>AgAaD+=**`{WNhoEKRm-U?)L!D+urI(E+EP4>PH@F{m66ak(yz8)zK;~D2PZZ=u<F
8%0gwQH4C_-RI>D%;d}A~Q!IUvYIG7WSU7}Ikhrm5b5ZNfOu@nLzfSt9-85|D6^;EfX^0BmmVekHvyS
Zz-7895NPOB@{NT!ZNHC9epVPui0Dd}l^9>X;kYQTg|HcrouM7v5#@XSE3>%(+THdH5@J{IZU4NbrJN
i@Z1?D6NH_tO@dtX;aUaumI&G&O<xh=&Byb&^jIE0eM&mAfsuAO_SVo+9YZ^vfMHeZ!N(b9WjVTH|7D
3dzQL_IP}kqn9*6Z0}6clmc?dI$t*V&KGY?Vifi?m{7FibJYORAZAEH!g@Ly2l$$x#q*e@d5Ba9i)fK
Nz#9jStpr+xF_<TDtSxU-)S<|_TjOz&PI{Yal-#u|<O7MkaJeEa<cq=i3_II6i#}Z0p_faXFe8jceAb
cVX97S;8loLhl{uyX*c#x>e73fBXJd~d32_8}Xj#aL`etZ%o|j-M1=x635VxnysL|_Mlio<^0c?MjOv
&_0lL+$_L$e032^*^PPk2hLUaH<PNlH5-0%tnE4zg5Uh*x<GM2eCEtZ1<E_?UN{n(a9mUX|!^>vht{!
e5_$|KalddJ?=jy?RsY8nXr`&1|ZpVcN%d&N)ql$MTSDA1~i_B^Mac#)iVSI?|P5;}$d}WoC+;y2Tja
mM_Qx3$sQ*pw1LIkl1I?$6j@H7mFlV&nRCd#trWst9i<(Cd-b(d^~(_rbXsar<p@SKT!c=(rHEXBwC_
Sp#TBMKSjUz3JYX07-)e<d8<_t_ke&ob<M(;R4@U&RH01vJKe}|n9I^01og>2K{4fxh#T5LUh~cPu=s
tm1<8P%cCy(XZ?>M#8NWd<HL<|1ZK;f!oH^?388^b?D3g!c;p^8XuHFDKsbxxCv_*2Bv<*d)$a4fLhP
E7)KxswY)iuA`p=-`}>XlZaQt=^IQs*r69U-WPRR%HA5+^6<siAP^H0v%6%l9wz5QRP)#g(+h*bd?hF
WVRdL7TknSenpZf3>Aq-HwaN!0o)28aZFQrh0=ylA?Mnl2Y=yf7GA-E+?1FmU%6pmS|LQ31p)<vh7-$
CHwV`CA)qzxtfTJ)3fhRznxr(S0Ct3nRlnxXKw_&6UdbC{PpFBcl7&m@~<DyFDLIN@2{`iMSFezcH#@
IJ8503RZNbROCz(iBLSWR?s{(I0;<gcUwlCE_n2V4i2M{T(OYn#>9Su;+ZB?MAph(_G7<&rftk}t%RA
Q&Ed8gHEZrO-<72w|g%7wp={3}5%6;e2O)1{(VY=7?KLtS@k<}EYa}cZLVo59pTL6tqvTt*;tQ0q*e$
4>1`~*PecoR#H%2$Vup*L+y*IScoo|pAK3v5tvkU&*xg$6^`J72D}WUPVx+V~rhr`SGF2N?zjy4}adb
tYjNMEMeklBhguxzX*nJH2T8-MZ6tFQP7=<-+`xtr2j9jN?mBfTdv@93LMwh)r*FN3{sQ{LNQj^GC5f
^q-EVbN@h4eDUS4e*K$6|LFzxEpUPU!vSZ9{?l~vo!H@wC=>uwWkFsH=to_^gsb4uolUguytYO58YTr
gm6Z%1u83Ii5iir$|7r{X3TAkUuRcn$k-z|GK?~7ACINxrSa4D)P^m!XU~w#6>7km|gt_MiF&x}j<Zs
QzQUi}E?+u+Cq)ysfVbV+-7|)gfjVvRny5O0&kPiqg)u0vg=M#{4_d+jK_eB2(GtWG?Jh;g)jm|KKTd
|Q_&&>`P)cT<6v_pr9>QUPKw6U_lA*2t&jb$5b+IE_|YnQci4?V?v7i(}&GhNnvXi?vaI@M<eq6n0$m
Ye3Z*q9+36-8j`1Y@J>*g2w!)rx0$VcPq={6@YdhicG0{#m2-`??w#9d*u#=oBaVV_e<cI0j1M`dQVz
&ap9!Hb?eGw<!-IV<-PO<Ndn-<{F)dvyI&A-+Y?lll8v+)uqG66nw^<YH#sN^W{tzIMQeH)lVvGGL8<
z-FY%t+h+mH76bLL1z`7V>YiJtbfH^Aqpy*1u-sJy+!@C=8jy>q-2GFZk?3%Wy<3G2(QRC)RE7||n!G
;!`1U%O{NZ|X`Tq3n+dl^HPTzwO`6`%PUVgZwu|4mHBea+Gu5b^iu-&jxYvr?Sp>oh=n87fpI@y=Upb
Dx|wBeZbj-W}>3fj|kS>i&Ql;})qH%8#Se>QGKy1{q=Sb;J-Dr@B2<IQxTB8C${n;UBp(+Up$`lOn^&
rt8`iADPzPh?W}*n5x^i4;{ufsh-cD2Eh=I!{!v9t;Oas|=G<K`M~*4o@n6_0@0h0`j-S-Ce!FW4*w4
cP-I^H<T@8bgykXTreH~aPhKyJFTWuEDESrJ@=hyqg9KF>(1dX%-isC_M^7zJ}<g*%aUNMNicSZw7ZJ
3Ew@m(^;gx|Id%m=eXkPLr9HWU_LbDNV6|o7K}Be~7V9Y{*-;hKdy~rE(l6~BPGy=%a{G1J3p&PScrU
F_NQKw1?<j=ZQ}flgUxDZ!u9`=#bk+d`Ll2BU0w!qxVHUoCR)o$7Yt$(^mZ*EQ<)^@G_b5IH6+Lbbv@
R+m+)JyFgXZHg0WygWlcL{$bbi+<V%VF{JVlHjzf+i`i#TyovpL$cLA~aIUh{xYSKP}r*p|rW=E_szd
^b4z_AGcexw@j*0j0*p#fPi&KbX53n4D(<6Xr3P(=1cyP#6}!HO^~-xF|7tW{T-0D>$2EWRAhJ1ao~3
@%Kp<=Z}g`B^S~GRT0^_U_y6Dbb`lRzG}n?-7TB^Xyq8#aYzXlSXKbbViLeO4l{H#rm%`eeDMXf;}lD
X`C3#Pjv*=SK;vr^!N<Ua5=f`9M87aB>mz#_0A6{QV-ZOxGWiI7Xpzd~!3outMeCL+OPv#qlkY50El(
)4Bu-1-EPST0RW=l6^L}e?k5s}=BN5btgLlQ>1_rTa{ZNRvitN8iW#$of;|(@$)veCxdY%<>-M|~;5z
)YFxkC8IhdxJq@=xOjz<ji2==MsG@~dt|u)f%fdUb&kwR4P{R9%m|g}Od<+POt+;uMYljtq#_{-kPTR
<*T2#R9SV2fZ{`LF&7Z{R{YXFN|dudY^IPIMr;9^YwqVb<P$d9YHMyWE!n<7I-JkSb2vhH2~Dx0|p5S
HDkZ}#H-5L__wWkYEvb2qWj+TC~ohz!wUL#2rP0tNU(Jml`Osb{%Ie5KXB^Q;5)f?4Yu~5i2$T(pmD!
}A)Ld=ddC?sZ2~FPZaMgHrORDmWwG}6mBfGbv&PC?@M+#Y{C4KXf;6{xTz@~g{02sA2B83r0FN)}JCk
9UL`^6Y8o$nqf$r1t`MIIK<#gb2MKa1rvf2Joc?R>5g@0ncbli9(CUaKpziU0K6X}-{9q`>|b;I<lOy
_Zyj|=KKCXaaEH7d=c{N1}B`fNabc)8FQB$&3oec?(#QgF6MUbx)>X;`{ev?~U2hmO^z0lNqv`96Y^l
jaK@t7ys11=otvfd_Ofm$0lo1{>N)OUk@WrM-4TS1uZd3Z(Z#682uKHJBm(_L$mu40|+^K>PX$EJcik
g&X)6?{oI(420LRg!UQ2&Q$usOxI4f;4xJ7(Q-7;HkR1ioi?Jr$DX_!x-FYitCpMGd_>!xd+w<anuNW
tpdO;Jq}w)ij6vRe*uvuWQq|cKj2P)OWcyqjQ!UHI<>c(c<tvT^AmQrkEp~9;p~mc@ae}Gd+;8PPjMl
ijNJ8n5+_N`#YygbyQjhDRFzooV?ezbnMLp*#AYo_fFtxq{i5zhJ|6$NkZoWS!LT?=p)AX>qDc_a)mT
pe%fUA~scoW#3Up&%wNKu|sL4V2x)CE@T_5rpNK9oP20mI?Z{{m1;0|XQR000O8X0rTPCjg_T=l}o!Q
~>}06#xJLaA|NaUukZ1WpZv|Y%gtLX>KlXc|DN9YQr!LhVOm~k<$vDeHm;EY{#9(cG<0z;wDNWaBLwd
8+rS=DXkDlNaEMWKS-IuR;D}x&0NIblhpR`%|<21<eckqfH_irh%#z>-yAN72Q@h!;SIh@#vMGq17&L
+)M%RKXCj4~ET|~I*uzi+O6s92SxZ9DPKZsxrfBua3Tl)RoDl>E6wF;E+vLc++nSFm5&NF56wsqZO1c
L{gvpGx4Phjkmb3559C+mzm^hH?f*PKmUSIqTaI3?`gL>gll^vyu`lV8+$8554sZ+g~bNZ9WjB-U0v_
<lLxEZu_|4>T<1QY-O00;nPviw+K)qGvx2><|h8~^|s0001RX>c!JX>N37a&BR4FK~Hqa&Ky7V{|TXd
DU6pZ`?QzexJWW=RRZ%%s371ipvf#J?vt;xB%U~U|V1xf?%Mr<ry^|%O}Z6jiUeik(6Xh^P}5+yrMv2
o1{pJ{P;<chfZnBB>iaQw&<;FX6}(G6Mi#;nbleySgD#ulvb+NcqP{IgQ#rZHNuJ5p_A<{eEqQ<7VNz
=cESGBp&oB$Gg+g>;#p_|Z#J^66??m8^S>|H%}u_VG5F{8tvWQ|*Gx1<xDT{QC%a<vEZR!xSW+@>MwQ
vIWYO{RiSNL>LW}?QQj3FV?HI^i`^+0z{XTt)O~}>?4c-^xb1Awc19S50t~Hi74aZOKv{riIUz64Q;a
;mxkh-6G*@QKW6Zusd15RBM$<KL#`(&nof-5^=H#!brR*9Nzq}epE2OCvyjMa0s{j|cJ$=UKP+bY$#%
xYnK-7*QzKqze~P;kLeGiSW57=$;EzDg?&3kC*rR^vXvBa<xyrQ9!k;7?-H4V{Z?({a0>_bqxYs*O>-
F2$w-UrVd>uyUrrCHR?mq%cyuFFq;RUe;f*Y+S0qBFNAUO6G^bfO9_!%OPuQ9o4McyX;gdTd;@BrxG8
sEw0*D_-nZr<x}*I0?Qs}A?!x+DheBYaqIL3(jmGxH~(CX?eKsb@VH>9JS78?3km4Jlz#+&Ht0J&&L~
%-nbQy+T@te_dk+pVyB91?5UXV)iWy1Wa}9=}x{T9G-DOMmZ)`0v0WUQ=(hFFsV)yUv847^iQcxZLi~
XirF&at!9RzP9Gkb2@E6c>^u92m*&A?12N?A)$6{CSPG2qF2RZ^ERRlA_v=PPqAywOZZ<u?tGPys@TY
Dhb%egtv))vHF$#$Lpg7EvPD9NOYs9t6SzsA9{4T<&(@cPjQM{g_4uSotED*{i;(Fln@EBX+zT0F5hH
4{C406uj0i625chz&Kc$Cmtlg=Wr#-*&>k+k%mq7^}e`la`Kg$gmK7-bjS$B!fPlnOfrUjl9|4v;I>%
EOtjBZtCmnK78=`~0!OqT2LS3i2VG=y|FlHOd~vd#7Kql*0&PTPz_e0!D!)855&eXUojMzkBtVliSTX
aoR`XGX>grTH)TFNf*y~o=qcsqC!&{P{3Pf|<@RPxl?s%Pj3HAGxRZ1AL#=A~%jgfD$WbOyMhko#Du2
^<tq7@Pgj9rBWxdJQjm=@0!%z?hGiY!WA2rLO|3gHFpGS!LpD0K@c04Q%LlXceHdU>1WINR%0;#k)?O
jw7ZUm*0Fc?|=eSMxj{rKzYkhTsvzy<!3La-Pw*rTdmSm5FYgQ6_k!kFN+1Y9K}G1slHP2J(C8jipxg
ZR17%5WXjHSVqvg6{y;(c1aD7`(1Nbe}FF~cP-DYgHCU11keaMCrDl{TeXDGOSeG5$V;Fhy<o2)i{6O
pI%Pl{YTy@K54;CNEX!WAm%V6d5vL>#R>rfeK>As7aM7EHniNE}<l6@DLIW_hwcHVi!ZHN4^Qs>k4e{
a$aK&4JS!NYZ!Flc{J|+a5LAJAlD1lS}`vG`%c6;s68{sc6&KB6Wx&~yU>`T`VW9soC8q+D#eNVp;TK
p^x<O0JuosYPrbgb~W(MUIhF!t)6KVy%E)=O2U5|4sfvyZwLzLFu{q<