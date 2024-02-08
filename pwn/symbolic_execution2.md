# symbolic_execution2

## 개요
 - symbolic_execution 문제 입니다.
 - exploit 코드에서 수정할 부분이있으니 혹시라도 참고하실분들은 참고하셔서 수정하셔서 사용하시길바랍니다.

## decompile
<img width="1270" alt="image" src="https://github.com/ChCh0i/steel/assets/108965611/245c4921-5114-4368-ba93-45c433469435">


main
```
0040c914      void* fsbase
0040c914      int64_t rax = *(fsbase + 0x28)
0040c923      int32_t var_758 = 1
0040c92d      int32_t len = 0x10
0040c937      int64_t var_d8
0040c937      __builtin_memset(s: &var_d8, c: 0, n: 0xc8)
0040ca24      char const* const buf = "What's your guess\n"
0040ca32      char const* const buf_1 = "Congratulations!\n"
0040ca4d      void var_718
0040ca4d      __builtin_memset(s: &var_718, c: 0, n: 0x640)
0040ca57      char const* const buf_2 = "Nah,, Try harder\n"
0040ca6d      int64_t rcx
0040ca6d      int32_t fd = socket(2, 1, 0, rcx)
0040ca7f      if (fd s< 0)
0040ca8b          perror(s: "socket failed")
0040ca95          exit(status: 1)
0040ca95          noreturn
0040cac3      if (setsockopt(zx.q(fd), 1, 0xf, &var_758, 4) != 0)
0040cacf          perror(s: "setsockopt")
0040cad9          exit(status: 1)
0040cad9          noreturn
0040cade      int16_t addr = 2
0040cae7      int32_t var_724 = 0
0040cafb      uint16_t var_726 = htons(x: 0x7a69)
0040cb20      if (bind(zx.q(fd), &addr, 0x10, &addr) s< 0)
0040cb2c          perror(s: "bind failed")
0040cb36          exit(status: 1)
0040cb36          noreturn
0040cb4f      if (listen(zx.q(fd), 3) s< 0)
0040cb5b          perror(s: "listen")
0040cb65          exit(status: 1)
0040cb65          noreturn
0040cb83      int32_t fd_1 = accept(fd, addr: &addr, len: &len)
0040cb95      if (fd_1 s< 0)
0040cba1          perror(s: "accept")
0040cbab          exit(status: 1)
0040cbab          noreturn
0040cbd6      send(fd: fd_1, buf, len: strlen(buf), flags: 0)
0040cbf4      recv(fd: fd_1, buf: &var_d8, len: 0x58, flags: 0)
0040cbf9      int32_t var_744 = 0
0040cc16      if (strlen(&var_d8) != 0x58)
0040cc3e          send(fd: fd_1, buf: buf_2, len: strlen(buf_2), flags: 0)
0040cc48          sleep(seconds: 1)
0040cc55          close(fd: fd_1)
0040cd4a      for (int32_t i = 0; i u<= 0x15; i = i + 1)
0040ccbe          int32_t rdx_5 = sx.d(*(&var_d8 + zx.q(i << 2))) << 0x18 | sx.d(*(&var_d8 + zx.q((i << 2) + 1))) << 0x10 | sx.d(*(&var_d8 + zx.q((i << 2) + 2))) << 8
0040ccf8          if (chall(sx.d(*(&var_d8 + zx.q(i << 2 | 3))) | rdx_5, i) == 0)
0040cd20              send(fd: fd_1, buf: buf_2, len: strlen(buf_2), flags: 0)
0040cd2a              sleep(seconds: 1)
0040cd37              close(fd: fd_1)
0040cd70      sprintf(s: &var_718, format: "ACS{%s}", &var_d8, "ACS{%s}")
0040cd9b      send(fd: fd_1, buf: buf_1, len: strlen(buf_1), flags: 0)
0040cdc6      send(fd: fd_1, buf: &var_718, len: strlen(&var_718), flags: 0)
0040cdd0      sleep(seconds: 1)
0040cddd      close(fd: fd_1)
0040cdeb      *(fsbase + 0x28)
0040cdf4      if (rax == *(fsbase + 0x28))
0040cdfc          return 0
0040cdf6      __stack_chk_fail()
0040cdf6      noreturn
```

chall
```
00401491      int64_t rax_251
00401491      if (arg2 u> 0x15)
0040c8fe          label_40c8fe:
0040c8fe          rax_251 = 1
00401491      else
00401491          switch (arg2)
00401584              case 0
00401584                  int32_t rax_30 = ixor(bswap(bswap(sub(add(bswap(anti_symex(add(sub(anti_symex(bswap(anti_symex(bswap(arg1), 0xc48cf0de)), 0xc217e3ee), 0x9362d33b), 0x92d10802), 0xb123eadb)), 0x9019aaef), 0x401eea24))), 0x495afb5d)
00401645                  int32_t rax_52 = ixor(sub(bswap(anti_symex(anti_symex(ixor(anti_symex(add(ixor(ixor(ixor(rax_30, 0x5809166c), 0xddc39ba7), 0x46b6d5f6), 0x8253211f), 0xba00c651), 0xe9a5740a), 0x9a762e3b), 0x63af9c8b)), 0x6b86a181), 0xf94c90e2)
0040170e                  int32_t rax_76 = bswap(add(bswap(ixor(sub(anti_symex(add(bswap(anti_symex(anti_symex(anti_symex(ixor(rax_52, 0x99249b72), 0x5cce6239), 0xef0f24a4), 0xcccbbcd9)), 0x2fb39ee5), 0xd106f2a2), 0xb13d795b), 0xa5059123)), 0x465bb693))
004017d7                  int32_t rax_100 = bswap(sub(sub(add(sub(sub(bswap(add(ixor(sub(bswap(ixor(rax_76, 0xa70c5231)), 0xc2938fed), 0x3710703c), 0x4ae2d5a0)), 0x55f0b31f), 0xd5736d7b), 0x7440f227), 0xb1d1835c), 0x50657ff3))
004018a0                  int32_t rax_124 = sub(sub(anti_symex(bswap(bswap(ixor(anti_symex(bswap(sub(add(ixor(ixor(rax_100, 0xcd1f8423), 0x42e57eba), 0x56ad9ebc), 0xfbee1d47)), 0x51ba3140), 0xd592dd77))), 0x56edb2f7), 0x171ad2a0), 0x54587588)
00401969                  int32_t rax_148 = anti_symex(ixor(add(ixor(bswap(add(sub(bswap(bswap(add(add(add(rax_124, 0xab3ca5b5), 0x18aec55e), 0xa8eecd57))), 0xdc9e47e3), 0x44d7780d)), 0x4c357ea3), 0x1dee6755), 0x3aea96f2), 0xfe0b8ebb)
00401a37                  int32_t rax_172 = ixor(add(add(ixor(ixor(anti_symex(anti_symex(bswap(sub(ixor(bswap(sub(rax_148, 0xda5a949f)), 0x198c9816), 0xbcaeb3de)), 0x3819a342), 0x9fc4f630), 0x5ade4674), 0x139dcbf9), 0x8b58563a), 0x376d1fb8), 0xd0d74fcf)
00401b05                  int32_t rax_196 = sub(bswap(add(sub(ixor(anti_symex(sub(add(sub(anti_symex(sub(bswap(rax_172), 0x863ca042), 0xee94940b), 0x60ca4f07), 0x655c8de2), 0xdaf03d49), 0x9586a778), 0x723b0d00), 0xe8501dd9), 0x62fae7a8)), 0x91bbc1a9)
00401bc6                  int32_t rax_218 = add(bswap(add(add(ixor(sub(sub(add(anti_symex(anti_symex(ixor(rax_196, 0x33e6e1fa), 0xa4a2ad23), 0xdc672521), 0xec85ec30), 0x531c4cd7), 0x4337b474), 0xcdd79faa), 0x4b645205), 0x7177e81f)), 0x3223e9a2)
00401c8f                  int32_t rax_242 = bswap(bswap(sub(sub(add(add(bswap(add(anti_symex(add(sub(add(rax_218, 0xf7a7d958), 0x66eaed9b), 0xbd5d93f9), 0xe276c325), 0x46e45736)), 0x47b03909), 0xfb9c9bef), 0x8cb0931b), 0xceac70ed)))
00401ce2                  int32_t i
00401ce2                  for (i = 3; i s>= 0; i = i - 1)
00401cce                      if ((rax_242 u>> (i << 3).b).b != *(zx.q((arg2 << 2) - i + 3) + &target))
00401cce                          break
00401ce2                  if (i s< 0)
00401cd0                      goto label_40c8fe
00401cd0                  rax_251 = 0
00401daf              case 1
00401daf                  int32_t rax_275 = sub(bswap(add(add(add(sub(ixor(bswap(ixor(ixor(sub(sub(arg1, 0x5e3dd340), 0x8e41ffae), 0x37b37835), 0x4cbe9fcc)), 0x2bf218f1), 0x110d2e28), 0x24f5b33f), 0x62c276e7), 0xcd702d6c)), 0x70fb7073)
00401e70                  int32_t rax_297 = add(bswap(anti_symex(anti_symex(add(ixor(ixor(sub(sub(sub(sub(rax_275, 0xf0170403), 0xe601d8d3), 0x27d06647), 0x67400c2c), 0x56fe752c), 0x69a8064c), 0xc39e0b5e), 0x4258d4e9), 0x8746bbc7)), 0xcfbc6580)
00401f31                  int32_t rax_319 = anti_symex(ixor(anti_symex(add(add(ixor(bswap(add(anti_symex(anti_symex(add(rax_297, 0xbdb78f59), 0x376e6701), 0xd522bae2), 0x5c1936a0)), 0x568ca257), 0xf1004703), 0xbc025fd7), 0x84c967c0), 0x4332790c), 0xf8150d31)
00402002                  int32_t rax_345 = ixor(ixor(ixor(bswap(bswap(sub(bswap(ixor(add(bswap(sub(bswap(ixor(rax_319, 0x3535d901)), 0xf6d11e8e)), 0x69ff2a95), 0xb0b42fce)), 0x557da445))), 0xf8c7b4c6), 0x87971554), 0xbe1a15f5)
004020cb                  int32_t rax_369 = bswap(ixor(bswap(ixor(add(anti_symex(ixor(anti_symex(ixor(bswap(ixor(add(rax_345, 0xcfe3b280), 0x433eaabd)), 0x94970ec4), 0xfd804dc7), 0x9f57d10a), 0x13eed062), 0x9d45e379), 0xc2e2de91)), 0xdb7d5e01))
0040218f                  int32_t rax_393 = bswap(ixor(add(anti_symex(ixor(bswap(add(add(add(bswap(sub(bswap(rax_369), 0x9bb0eef1)), 0xfb27b977), 0xec7bb4ea), 0x548388ea)), 0x70428a36), 0x6cccbef3), 0x3c55432c), 0x4e94851c))
0040225d                  int32_t rax_417 = anti_symex(anti_symex(add(anti_symex(sub(ixor(anti_symex(bswap(ixor(bswap(ixor(ixor(rax_393, 0x4201f187), 0xee87e597)), 0xb9d20eb9)), 0x6238f309), 0x86716324), 0x62df37d5), 0xb062937f), 0x53691eba), 0xd9f52331), 0x51d063f1)
00402326                  int32_t rax_441 = add(anti_symex(bswap(bswap(anti_symex(sub(add(bswap(add(add(anti_symex(sub(rax_417, 0xda49d08d), 0xb2b1cfc2), 0x96a017aa), 0x7d7dc998)), 0x9e57bf5e), 0x422634fd), 0xcf2277b4))), 0xa97dee21), 0x27a6cfd9)
004023f2                  int32_t rax_467 = anti_symex(ixor(add(sub(bswap(bswap(bswap(bswap(bswap(bswap(add(sub(add(rax_441, 0xe9d12b18), 0x2004f8c3), 0x4de44944))))))), 0x9458ceb8), 0x4c9ffd04), 0xcca6737a), 0xa492646e)
004024bb                  int32_t rax_491 = bswap(bswap(bswap(add(ixor(add(ixor(sub(sub(add(anti_symex(ixor(rax_467, 0xe2ce5d00), 0x38d5528a), 0x38dd24d1), 0xcd163b82), 0xcde54bd1), 0xbb953557), 0x3f37d73c), 0x40098858), 0xecce0d0e))))
0040250e                  int32_t i_1
0040250e                  for (i_1 = 3; i_1 s>= 0; i_1 = i_1 - 1)
004024fa                      if ((rax_491 u>> (i_1 << 3).b).b != *(zx.q((arg2 << 2) - i_1 + 3) + &target))
004024fa                          break
0040250e                  if (i_1 s< 0)
004024fc                      goto label_40c8fe
004024fc                  rax_251 = 0
004025de              case 2
004025de                  int32_t rax_525 = sub(sub(add(bswap(bswap(sub(sub(anti_symex(bswap(ixor(bswap(bswap(anti_symex(arg1, 0xa91579bd))), 0x32a49eba)), 0x51fca074), 0x17a42682), 0xa3f823bf))), 0xacb8d57d), 0xf1fd1c4b), 0x6230fb5b)
004026a2                  int32_t rax_549 = sub(anti_symex(bswap(anti_symex(ixor(add(bswap(bswap(bswap(anti_symex(add(add(rax_525, 0x93e68af4), 0xd57bc5da), 0xfe980323)))), 0x78435865), 0x84e42a8c), 0xa21c8510)), 0x4376ae28), 0x9aa6a594)
00402770                  int32_t rax_573 = anti_symex(ixor(bswap(ixor(ixor(anti_symex(ixor(ixor(ixor(bswap(ixor(anti_symex(rax_549, 0xf5e184ed), 0x59e4879a)), 0xf43b0800), 0xa399a70e), 0xe02d3a97), 0x4c2b5a69), 0x67fc1ef0), 0x749c1303)), 0x64168a4b), 0x5ffaf319)
00402839                  int32_t rax_597 = add(anti_symex(bswap(bswap(ixor(bswap(sub(add(sub(add(add(sub(rax_573, 0x4b60d4ba), 0x21a14fdd), 0x66b845e0), 0xd3efd135), 0x3cf171e4), 0xd6e9128a)), 0xd8dc81eb))), 0x1da61d50), 0x5214c32d)
00402902                  int32_t rax_621 = add(ixor(sub(anti_symex(ixor(bswap(bswap(sub(sub(anti_symex(anti_symex(bswap(rax_597), 0x5ba8ebd6), 0x23304941), 0xf7ac689d), 0x50c2a37b))), 0x13c59e6f), 0x3c7b5dfb), 0xf1c9573f), 0x982cfd00), 0xffd0080e)
004029d0                  int32_t rax_645 = ixor(bswap(ixor(add(bswap(anti_symex(add(anti_symex(anti_symex(add(anti_symex(ixor(rax_621, 0x6005aef9), 0x94963433), 0x1ea310f2), 0xf5bca9af), 0xda651a04), 0x3816e858), 0x268609cc)), 0x698e7a32), 0x6723b1e1)), 0x4548e527)
00402a91                  int32_t rax_667 = add(sub(ixor(sub(ixor(sub(ixor(anti_symex(bswap(sub(anti_symex(rax_645, 0x8f327eaf), 0x53963d02)), 0x648c1c75), 0xb35495bc), 0x8c8992ac), 0x7be3073d), 0x275e3d7c), 0x472cb59c), 0x62f80761), 0x407bfa23)
00402b5a                  int32_t rax_691 = add(sub(add(sub(sub(bswap(anti_symex(add(bswap(sub(bswap(anti_symex(rax_667, 0xbb5b1138)), 0x6bf1ebfb)), 0xe6401e6b), 0x66abc702)), 0xf5aeb6be), 0xed3e0c64), 0x5df5e096), 0xf5954c18), 0x1262fe15)
00402c23                  int32_t rax_715 = add(ixor(add(add(add(bswap(bswap(add(add(sub(bswap(sub(rax_691, 0x672c5539)), 0x196a6ac6), 0xb59c7f8e), 0x17096149))), 0x6ed4e2db), 0x496e5fb0), 0x917c3507), 0x2f1d91f6), 0xf843ebc9)
00402cdf                  int32_t rax_737 = sub(sub(add(sub(add(sub(ixor(ixor(bswap(bswap(sub(rax_715, 0x9833dee5))), 0xb01ae57e), 0x8e17828d), 0xf2e01e08), 0xb06c2290), 0x1ac5e4f5), 0x76862690), 0x87388ae2), 0x5a44b2dd)
00402d32                  int32_t i_2
00402d32                  for (i_2 = 3; i_2 s>= 0; i_2 = i_2 - 1)
00402d1e                      if ((rax_737 u>> (i_2 << 3).b).b != *(zx.q((arg2 << 2) - i_2 + 3) + &target))
00402d1e                          break
00402d32                  if (i_2 s< 0)
00402d20                      goto label_40c8fe
00402d20                  rax_251 = 0
00402e02              case 3
00402e02                  int32_t rax_771 = ixor(bswap(add(add(sub(bswap(ixor(bswap(add(add(bswap(sub(bswap(arg1), 0xb866c1d3)), 0x4d9705d0), 0xb663fde2)), 0x809e37b6)), 0x52a10dc4), 0x888c9a39), 0x4f7aa3a1)), 0xb3419443)
00402ecb                  int32_t rax_795 = add(bswap(ixor(sub(bswap(anti_symex(bswap(ixor(anti_symex(sub(ixor(anti_symex(rax_771, 0x2933baa3), 0xd2801baf), 0x6b9d91eb), 0xf4152e83), 0xb813bbfd)), 0x569e1fc3)), 0x3dd4cc2e), 0xe891bb1c)), 0x80be8ccb)
00402f94                  int32_t rax_819 = sub(sub(add(bswap(anti_symex(anti_symex(bswap(anti_symex(add(bswap(sub(anti_symex(rax_795, 0x1c463f08), 0xa4175847)), 0x6709521f), 0xf53b15d7)), 0x293cacab), 0x917b3db7)), 0x856d9171), 0x2802c247), 0xa3428bb2)
0040305d                  int32_t rax_843 = add(anti_symex(bswap(ixor(bswap(bswap(anti_symex(add(anti_symex(ixor(ixor(ixor(rax_819, 0xcae51d74), 0x81df0994), 0xfb915153), 0xbc465d5d), 0xace8d5c7), 0x78c2c8ae))), 0xd15af45b)), 0xb38aa917), 0xe44362b2)
0040312b                  int32_t rax_867 = add(add(anti_symex(sub(add(sub(add(anti_symex(bswap(anti_symex(bswap(add(rax_843, 0x9ad00d0e)), 0xc084faab)), 0x5c31b622), 0x98d8edbd), 0x33f0ca34), 0x631836e0), 0x3fed3c51), 0x2370baaa), 0xafe3e807), 0x1e9cd743)
004031f9                  int32_t rax_891 = add(ixor(add(sub(ixor(ixor(anti_symex(bswap(sub(add(bswap(add(rax_867, 0xc5176ca6)), 0xe94393f2), 0x5b32a00f)), 0xcceebf6e), 0xa6c1b211), 0xe71912e3), 0x3fea47ea), 0x35ec206a), 0x8ca32ae2), 0x7c69aaab)
004032bd                  int32_t rax_915 = bswap(sub(bswap(ixor(ixor(add(sub(ixor(bswap(bswap(anti_symex(ixor(rax_891, 0x2f6f9d0f), 0x80b78e21))), 0xc8bccb9f), 0xf0bb7480), 0xd8e2e747), 0xd7cc587f), 0xb92e6251)), 0xafcb939c))
00403386                  int32_t rax_939 = bswap(anti_symex(add(anti_symex(bswap(sub(ixor(add(sub(bswap(sub(ixor(rax_915, 0x58d030d3), 0xc4cf2815)), 0xb376938c), 0x2655a6f1), 0x50efc0ee), 0xd93a29e6)), 0x58620c6d), 0xa7bba02d), 0xa58cce3b))
00403447                  int32_t rax_961 = add(bswap(sub(ixor(add(ixor(sub(ixor(sub(anti_symex(sub(rax_939, 0xfa8d2603), 0xfb1f5743), 0xc9231866), 0x2b81495f), 0x3e94e2bd), 0xbc49b4ac), 0xd26aaf24), 0xed40be80), 0xcaeb7933)), 0x3f0851dd)
004034fe                  int32_t rax_983 = ixor(bswap(sub(sub(bswap(sub(ixor(ixor(bswap(anti_symex(anti_symex(rax_961, 0xe359f851), 0x23f4efbd)), 0x6bc03913), 0x6d35ce2f), 0x91daf9da)), 0x28a93a80), 0xbbff3a2a)), 0x9299e723)
00403551                  int32_t i_3
00403551                  for (i_3 = 3; i_3 s>= 0; i_3 = i_3 - 1)
0040353d                      if ((rax_983 u>> (i_3 << 3).b).b != *(zx.q((arg2 << 2) - i_3 + 3) + &target))
0040353d                          break
00403551                  if (i_3 s< 0)
0040353f                      goto label_40c8fe
0040353f                  rax_251 = 0
00403619              case 4
00403619                  int32_t rax_1015 = bswap(anti_symex(anti_symex(sub(sub(add(sub(sub(add(bswap(bswap(ixor(arg1, 0xece26215))), 0x225935d7), 0xc6700029), 0x8aca0b74), 0xe960e9bc), 0x9337635d), 0xb8217d58), 0xef6d3035), 0xdd63d795))
004036e2                  int32_t rax_1039 = bswap(ixor(sub(ixor(ixor(ixor(add(sub(add(bswap(add(bswap(rax_1015), 0x93ed8dd6)), 0x62c725d8), 0xb0352459), 0xf3f6761f), 0xe8993978), 0x8161afd0), 0x228b6c58), 0x2f8b524f), 0xcaedd932))
004037a8                  int32_t rax_1061 = sub(ixor(add(ixor(anti_symex(add(sub(sub(ixor(anti_symex(anti_symex(rax_1039, 0xad22e458), 0x2d29ca60), 0x10b51ba2), 0xad3e59f0), 0xf6c126f6), 0x58b22918), 0x7732271e), 0x62aa5e3f), 0xf9008ae9), 0xf434fba6), 0x60e613cf)
00403876                  int32_t rax_1085 = sub(anti_symex(bswap(bswap(add(anti_symex(anti_symex(sub(add(anti_symex(add(anti_symex(rax_1061, 0x4837c76a), 0xfeeb2162), 0xf0375f81), 0x33d90e39), 0x480b3d55), 0xe68d16a1), 0x8a49d5ad), 0x3b896416))), 0x80e7d770), 0x9c002b7a)
00403944                  int32_t rax_1109 = add(anti_symex(sub(add(bswap(add(anti_symex(bswap(add(ixor(anti_symex(add(rax_1085, 0x59197cc6), 0x8b875b36), 0x65aeba48), 0x8b638216)), 0x98cd8182), 0x2ec8558d)), 0x839042e8), 0xf2fd8c98), 0x3938f915), 0xd8a738b3)
00403a0a                  int32_t rax_1131 = sub(ixor(add(add(ixor(sub(add(ixor(ixor(add(add(rax_1109, 0x70055f52), 0x30bd202e), 0xdd830106), 0x61576dcf), 0xf86ac992), 0xdd1a9555), 0xd6d47326), 0x79db839e), 0x234a0d12), 0x943c6ddb), 0x3d24585b)
00403ad3                  int32_t rax_1155 = add(add(bswap(bswap(sub(anti_symex(sub(ixor(add(sub(ixor(bswap(rax_1131), 0xa42b0f1f), 0x514c8555), 0xf6b23ffb), 0x3eaaf548), 0xa9d088d8), 0x3ac7e751), 0xda91f8ac))), 0x92d80640), 0x77448298)
00403b9c                  int32_t rax_1179 = sub(ixor(bswap(add(ixor(bswap(anti_symex(add(bswap(anti_symex(anti_symex(add(rax_1155, 0x5da04891), 0x1e184eff), 0x2301151b)), 0xa52b4159), 0x4b9bf893)), 0x939893f2), 0x8d367bc5)), 0xb5b59cde), 0x9c8d2547)
00403c5d                  int32_t rax_1201 = sub(bswap(sub(anti_symex(ixor(anti_symex(sub(sub(add(sub(anti_symex(rax_1179, 0xf0ba1a89), 0x402c16f9), 0x5a2b8f5e), 0xd9484bea), 0xac58abe9), 0xfe1d6044), 0x784fbd26), 0x2f783a71), 0x6a0f9691)), 0x259a939c)
00403d23                  int32_t rax_1223 = add(ixor(add(sub(ixor(add(sub(add(add(add(sub(rax_1201, 0x61852963), 0xb73e850c), 0xcac852de), 0x7a4fdfd8), 0x44574fa5), 0xe688f0cc), 0x6c625617), 0x7839a9db), 0xbe69571b), 0x8afda7f3), 0x789fa9d1)
00403d59                  int32_t rax_1229 = ixor(sub(add(rax_1223, 0xd00d507a), 0x563107a1), 0x630ca639)
00403dac                  int32_t i_4
00403dac                  for (i_4 = 3; i_4 s>= 0; i_4 = i_4 - 1)
00403d98                      if ((rax_1229 u>> (i_4 << 3).b).b != *(zx.q((arg2 << 2) - i_4 + 3) + &target))
00403d98                          break
00403dac                  if (i_4 s< 0)
00403d9a                      goto label_40c8fe
00403d9a                  rax_251 = 0
00403e71              case 5
00403e71                  int32_t rax_1259 = anti_symex(sub(sub(sub(anti_symex(anti_symex(add(sub(sub(anti_symex(sub(arg1, 0x7be42ae8), 0xcdfb4688), 0x835920f5), 0x6c7eac27), 0x839caaea), 0x8e8f7c07), 0xb4a167db), 0xc1c736c4), 0x7aa90c11), 0xa22a5cea), 0x95c6ace3)
00403f3f                  int32_t rax_1283 = anti_symex(bswap(anti_symex(sub(anti_symex(ixor(ixor(sub(add(bswap(anti_symex(anti_symex(rax_1259, 0x3248dfe2), 0xfccd1806)), 0xe4b9052b), 0x7ff78ce5), 0xa4d4ca62), 0x861b1dbe), 0x6d1c3912), 0x1179a4c5), 0xdb951e59)), 0xe878000b)
0040400d                  int32_t rax_1307 = ixor(anti_symex(sub(bswap(sub(anti_symex(bswap(add(anti_symex(ixor(add(add(rax_1283, 0x2fb0f455), 0xc9d11415), 0x748d7525), 0xea92fa48), 0xe8679d2c)), 0xee7f4cda), 0x830c3952)), 0x7a28771c), 0x6476a633), 0x1cbe5c46)
004040d1                  int32_t rax_1331 = anti_symex(bswap(bswap(bswap(add(ixor(sub(add(bswap(anti_symex(sub(anti_symex(rax_1307, 0x893d9125), 0x56c6a61a), 0x4f5e5b19)), 0xf45a7031), 0xe2c06e91), 0x1e0480c3), 0xe0519601)))), 0x39bdda20)
0040419d                  int32_t rax_1357 = bswap(bswap(bswap(bswap(bswap(sub(sub(ixor(anti_symex(ixor(add(bswap(sub(rax_1331, 0x4458c61a)), 0xb03a665c), 0x305265bd), 0xcdf6689a), 0x8be55f33), 0xa6a59649), 0x77a002f5))))))
00404266                  int32_t rax_1381 = bswap(sub(ixor(bswap(ixor(add(ixor(bswap(anti_symex(add(anti_symex(anti_symex(rax_1357, 0x2ec6a4e1), 0x1a473061), 0x2c95e15a), 0x9d04a74d)), 0x8ca9aec5), 0x54a1daaa), 0x74a3979c)), 0xb50befbc), 0xde70160f))
0040432a                  int32_t rax_1405 = add(sub(bswap(bswap(ixor(add(ixor(bswap(anti_symex(ixor(bswap(sub(rax_1381, 0xdaef56b6)), 0xb58d2746), 0x3b7fffdb)), 0xfb7d0004), 0x9ce069f3), 0x7b32a9f4))), 0x89c44106), 0xb4fcb084)
004043fb                  int32_t rax_1431 = sub(bswap(add(bswap(add(ixor(bswap(add(bswap(add(add(bswap(sub(rax_1405, 0xbf6c6af1)), 0x3f253901), 0xb5fe21cd)), 0xaf6c910b)), 0x6edbc38e), 0x1d553876)), 0x279f2b5d)), 0xd548fcee)
004044bc                  int32_t rax_1453 = sub(bswap(ixor(sub(sub(sub(sub(ixor(sub(add(ixor(rax_1431, 0x67b562ab), 0xdc77dd94), 0xa930bb3a), 0x9e28e2cb), 0x65237fc7), 0x49ac256e), 0x1dadb881), 0xca26dba7), 0xed539e8c)), 0xfb868070)
0040456e                  int32_t rax_1475 = sub(bswap(add(bswap(add(sub(sub(bswap(bswap(add(ixor(rax_1453, 0x68cf7033), 0xdd4a51bf))), 0xd3026ec7), 0x46c65873), 0x887dbd88)), 0xbb722342)), 0xba9ea776)
004045c1                  int32_t i_5
004045c1                  for (i_5 = 3; i_5 s>= 0; i_5 = i_5 - 1)
004045ad                      if ((rax_1475 u>> (i_5 << 3).b).b != *(zx.q((arg2 << 2) - i_5 + 3) + &target))
004045ad                          break
004045c1                  if (i_5 s< 0)
004045af                      goto label_40c8fe
004045af                  rax_251 = 0
00404689              case 6
00404689                  int32_t rax_1507 = add(bswap(bswap(bswap(add(anti_symex(add(add(sub(add(add(anti_symex(arg1, 0xdeaf2ae5), 0x26498625), 0x88294a15), 0x4315918f), 0x714a3a04), 0x901fb760), 0x3890439f), 0xc2920c37)))), 0x6eae5e9f)
0040475a                  int32_t rax_1533 = add(bswap(ixor(anti_symex(add(bswap(sub(add(bswap(sub(add(bswap(bswap(rax_1507)), 0x67bd8d74), 0xcc03fdfb)), 0x16ea8de1), 0x4b180ecb)), 0x70c194d0), 0x46058df6), 0x550ea0de)), 0xd12eb1db)
0040481b                  int32_t rax_1555 = add(bswap(sub(anti_symex(ixor(sub(sub(sub(ixor(ixor(sub(rax_1533, 0xf2109c51), 0x2c32c0bf), 0x8115aa2e), 0xe91033b8), 0x876ad41b), 0x6ca734e6), 0xc9b459f1), 0x21a80845), 0x7c4cace6)), 0x146e5a7c)
004048df                  int32_t rax_1579 = ixor(ixor(sub(bswap(add(bswap(sub(sub(bswap(add(bswap(add(rax_1555, 0x397e96af)), 0xa87ddb5d)), 0x6539c97e), 0xea2b35ba)), 0x1eefcb5e)), 0x157bee49), 0x691635f8), 0xf941442b)
004049a8                  int32_t rax_1603 = bswap(ixor(anti_symex(anti_symex(sub(add(bswap(add(add(add(bswap(ixor(rax_1579, 0x2bf0e91d)), 0x884eb23f), 0xf2f2c97c), 0x4b2ed0ef)), 0x35c239db), 0xe57f0e25), 0x416b4959), 0x65432a67), 0xf986591d))
00404a71                  int32_t rax_1627 = add(ixor(sub(ixor(ixor(bswap(anti_symex(anti_symex(bswap(bswap(sub(sub(rax_1603, 0x4a61137f), 0xe6f3617b))), 0xec02f67c), 0x25ae6a57)), 0xf1710f1a), 0xb89fa513), 0xd317d2cd), 0x675f08e6), 0x62a87442)
00404b45                  int32_t rax_1655 = ixor(bswap(sub(bswap(bswap(bswap(anti_symex(bswap(add(anti_symex(bswap(bswap(add(bswap(rax_1627), 0x43fdd0ab))), 0x30dba859), 0xf0a3f537)), 0x437ca48c)))), 0x712880d9)), 0x4c35fe0f)
00404c0e                  int32_t rax_1679 = sub(bswap(anti_symex(add(add(anti_symex(ixor(anti_symex(add(ixor(bswap(bswap(rax_1655)), 0x9797002d), 0x7441dad5), 0x14d83237), 0x1ac2bae7), 0x7888c0a7), 0xe5ed5696), 0x723a5252), 0x938b6d81)), 0x845d81c4)
00404ccf                  int32_t rax_1701 = anti_symex(sub(add(anti_symex(ixor(ixor(anti_symex(sub(add(bswap(sub(rax_1679, 0xdba3ab0f)), 0xf1067764), 0x43128737), 0x76020b72), 0x38fb183a), 0xbfc9216d), 0x321d9a0a), 0xee1e8a3a), 0x8a2bd506), 0xcd0691f4)
00404d90                  int32_t rax_1723 = sub(sub(sub(bswap(add(anti_symex(anti_symex(add(anti_symex(add(sub(rax_1701, 0x9bdba3da), 0x9cb42887), 0xeb2af1be), 0x4fd76df0), 0xff8f6780), 0x4fadab51), 0x1ea74b61)), 0x1a7cadba), 0xda143852), 0xbd45147f)
00404de3                  int32_t i_6
00404de3                  for (i_6 = 3; i_6 s>= 0; i_6 = i_6 - 1)
00404dcf                      if ((rax_1723 u>> (i_6 << 3).b).b != *(zx.q((arg2 << 2) - i_6 + 3) + &target))
00404dcf                          break
00404de3                  if (i_6 s< 0)
00404dd1                      goto label_40c8fe
00404dd1                  rax_251 = 0
00404ea6              case 7
00404ea6                  int32_t rax_1755 = bswap(bswap(ixor(add(ixor(anti_symex(ixor(add(bswap(bswap(add(sub(arg1, 0x9f201c58), 0xbe4502e2))), 0xcd1533b5), 0x802f657e), 0x1a81761d), 0x37814f04), 0x80388d71), 0x31d51c71)))
00404f77                  int32_t rax_1781 = anti_symex(add(ixor(ixor(bswap(sub(bswap(bswap(sub(bswap(add(add(bswap(rax_1755), 0xa9668e07), 0x44116fdb)), 0x775b6bbb))), 0xf07eb061)), 0xe6be0b6e), 0x52f0ed46), 0xf14d8f10), 0xcc5ec44d)
0040503b                  int32_t rax_1805 = ixor(bswap(ixor(ixor(bswap(sub(ixor(sub(ixor(sub(bswap(bswap(rax_1781)), 0x3134fb8d), 0x9d621b9b), 0x4ed24e12), 0x3f00c464), 0x5764527e)), 0x90400b77), 0xdef5e939)), 0x148a6b99)
004050fc                  int32_t rax_1827 = anti_symex(sub(ixor(bswap(anti_symex(add(ixor(add(ixor(sub(add(rax_1805, 0x45bd2ca0), 0xf8e34515), 0x5e728c29), 0xc10c2591), 0x20859b18), 0x692405ed), 0x43947ba6)), 0x715c7caf), 0x9d63cab4), 0x20243f2e)
004051c5                  int32_t rax_1851 = bswap(add(anti_symex(sub(bswap(bswap(ixor(add(ixor(sub(anti_symex(sub(rax_1827, 0x1717e73c), 0x1b8433ba), 0x51eabae8), 0xb5546a57), 0x1a3bfd5f), 0xc34aee37))), 0x5e94e3a4), 0xf635347f), 0x277af51b))
0040528b                  int32_t rax_1873 = sub(add(anti_symex(ixor(anti_symex(anti_symex(add(ixor(ixor(anti_symex(sub(rax_1851, 0x199e66ed), 0x1f7857a5), 0x630a25bb), 0xb09229f9), 0x4b946cac), 0x425f6c20), 0xa6765e1d), 0xb2136f26), 0x7c127e42), 0x7cab2b41), 0x867a1d09)
0040534c                  int32_t rax_1895 = add(bswap(ixor(sub(sub(sub(sub(sub(ixor(sub(ixor(rax_1873, 0xf21d3628), 0x4ed6cf2b), 0x5ac96dda), 0xbdd0e5b2), 0x16d852d9), 0x8ccb14c3), 0xb2986591), 0xfbb76dd2), 0x806bcd2c)), 0xe89736c4)
00405412                  int32_t rax_1917 = sub(anti_symex(sub(ixor(anti_symex(anti_symex(ixor(sub(add(add(anti_symex(rax_1895, 0xf7ace209), 0xb622400f), 0xee695287), 0x534d29c0), 0x7cc3d801), 0xfa5e5573), 0xd7103a66), 0x1fb59690), 0xb9903e4f), 0x746810ab), 0x2ece3756)
004054db                  int32_t rax_1941 = anti_symex(sub(bswap(anti_symex(bswap(anti_symex(add(ixor(sub(add(add(bswap(rax_1917), 0x708fbbc3), 0x1c20a993), 0xe5786000), 0xfce3265f), 0xb7f37174), 0x19b19232)), 0x8c900044)), 0x54801fcb), 0xaad31137)
004055a9                  int32_t rax_1965 = ixor(sub(sub(sub(anti_symex(ixor(add(bswap(ixor(sub(anti_symex(bswap(rax_1941), 0xf639b5bc), 0xa8995cc1), 0xc8d31557)), 0xca7c29ac), 0x4b0a856b), 0x9e433bf6), 0x8f551ecb), 0x18c5ec7b), 0x37865049), 0x71e9242a)
004055da                  int32_t rax_1971 = add(bswap(ixor(rax_1965, 0xf01d6d7f)), 0x5c235ccd)
0040562d                  int32_t i_7
0040562d                  for (i_7 = 3; i_7 s>= 0; i_7 = i_7 - 1)
00405619                      if ((rax_1971 u>> (i_7 << 3).b).b != *(zx.q((arg2 << 2) - i_7 + 3) + &target))
00405619                          break
0040562d                  if (i_7 s< 0)
0040561b                      goto label_40c8fe
0040561b                  rax_251 = 0
004056f5              case 8
004056f5                  int32_t rax_2003 = ixor(ixor(ixor(anti_symex(bswap(bswap(anti_symex(ixor(anti_symex(bswap(ixor(anti_symex(arg1, 0x2db4d272), 0x4f8aff11)), 0xe15fe668), 0x42ff331e), 0xa6af8efe))), 0x8ab9ca19), 0x5c683656), 0xeedd7d44), 0x55e7e52c)
004057c3                  int32_t rax_2027 = sub(anti_symex(anti_symex(add(bswap(ixor(anti_symex(anti_symex(anti_symex(sub(bswap(ixor(rax_2003, 0x4b1855ed)), 0xba083994), 0xd8e5e4a6), 0xbeff90ea), 0xff32e82c), 0x3dd75335)), 0xe4e18a93), 0xd98bba49), 0x9f64dfb6), 0xe5afdebf)
00405891                  int32_t rax_2051 = add(bswap(sub(add(add(sub(anti_symex(add(bswap(anti_symex(anti_symex(sub(rax_2027, 0xdc33628f), 0x67270bb6), 0xb18d3b3f)), 0xf4ce4fef), 0x46d57b65), 0xdab9be3b), 0x1967030e), 0x8201bf4c), 0x55e4ee4d)), 0x2a55a511)
0040595f                  int32_t rax_2075 = add(anti_symex(add(bswap(anti_symex(add(ixor(sub(sub(bswap(add(ixor(rax_2051, 0x340fae4c), 0x5a664d02)), 0xd44b29cb), 0xabb4cdd7), 0x8374548e), 0x6ba01a07), 0x6013fb83)), 0x4e340347), 0xf921637f), 0xfff4f69c)
00405a23                  int32_t rax_2099 = anti_symex(sub(add(bswap(add(bswap(bswap(bswap(add(anti_symex(ixor(ixor(rax_2075, 0x7679d248), 0x496171e2), 0xeb19893e), 0x189d5c1e)))), 0xf6c09c63)), 0xcd9de9b4), 0x1f179bf6), 0x11674f36)
00405ae9                  int32_t rax_2121 = sub(anti_symex(add(sub(add(anti_symex(sub(sub(sub(sub(ixor(rax_2099, 0x17e1621d), 0x55d437b2), 0x60911308), 0xb845fed7), 0xa82d7ca3), 0x2b32dfed), 0xb368a4b0), 0x6d58b96a), 0x9e5ecd4d), 0x48b3ddd7), 0x7f51f325)
00405baa                  int32_t rax_2143 = anti_symex(add(add(anti_symex(add(sub(bswap(sub(sub(ixor(ixor(rax_2121, 0x27793dac), 0xc5ff4cfa), 0x82b9050f), 0x1a1bd238)), 0xd9ac1d27), 0x26acf2c5), 0xb21d7f00), 0xbdc011fd), 0x80d5384b), 0x3f1fe4ab)
00405c6b                  int32_t rax_2165 = ixor(ixor(ixor(sub(sub(ixor(sub(bswap(ixor(sub(ixor(rax_2143, 0xca55f1b1), 0x15143b3b), 0x5f6f52ee)), 0x856d99ce), 0xe1629856), 0x47dca3a5), 0x49492d9a), 0xd6a19f50), 0x8bba6b7c), 0x3aa51642)
00405d37                  int32_t rax_2191 = bswap(bswap(sub(ixor(bswap(bswap(add(sub(bswap(sub(sub(bswap(sub(rax_2165, 0x8069d3e1)), 0x58b7a0de), 0xff5db90b)), 0x35eeb87e), 0x1d89cf9b))), 0x6418329b), 0xfd4ee5aa)))
00405e03                  int32_t rax_2217 = bswap(bswap(bswap(add(ixor(sub(bswap(bswap(ixor(sub(bswap(ixor(add(rax_2191, 0xde74b867), 0x2f977b7c)), 0xb6ca4951), 0xa76760e1))), 0xa53283bf), 0x17430145), 0x80f18fdf))))
00405e56                  int32_t i_8
00405e56                  for (i_8 = 3; i_8 s>= 0; i_8 = i_8 - 1)
00405e42                      if ((rax_2217 u>> (i_8 << 3).b).b != *(zx.q((arg2 << 2) - i_8 + 3) + &target))
00405e42                          break
00405e56                  if (i_8 s< 0)
00405e44                      goto label_40c8fe
00405e44                  rax_251 = 0
00405f19              case 9
00405f19                  int32_t rax_2249 = add(bswap(bswap(sub(anti_symex(bswap(add(ixor(ixor(bswap(sub(anti_symex(arg1, 0xcd2cda3c), 0x6a47297c)), 0xf8e953ff), 0x830527bf), 0x3f7e9dc4)), 0x5d5f864a), 0x531271cc))), 0x86b6114c)
00405fe7                  int32_t rax_2273 = add(add(add(sub(add(sub(bswap(add(bswap(add(sub(add(rax_2249, 0x60a1c202), 0x2ec50760), 0xce889110)), 0x8e26bd1d)), 0x1bd43231), 0x19d16dcc), 0x3ac5c85d), 0x4e219417), 0x17f98381), 0x532c69f6)
004060b0                  int32_t rax_2297 = anti_symex(sub(bswap(add(add(add(bswap(ixor(anti_symex(bswap(ixor(anti_symex(rax_2273, 0x20b4235f), 0x7953b8b7)), 0x40a589fd), 0x2681a8ba)), 0x91d18584), 0xf046fc98), 0xc677afa1)), 0xa29de2b3), 0xde9a2979)
00406179                  int32_t rax_2321 = sub(bswap(sub(sub(anti_symex(bswap(anti_symex(ixor(bswap(ixor(add(ixor(rax_2297, 0x9e232b31), 0xde2e7b8b), 0x238eb88c)), 0x54cf719d), 0xed038265)), 0x1cede014), 0x7af23be7), 0x56cee68a)), 0xae0eb1cd)
00406247                  int32_t rax_2345 = ixor(sub(bswap(add(anti_symex(sub(anti_symex(add(add(add(bswap(add(rax_2321, 0xf5ac9a78)), 0xc013e13f), 0xfc3d9447), 0x894b3357), 0xaea4c63f), 0xf491599a), 0xf6d5a6c4), 0x926549d0)), 0x1fc41941), 0x9ec28726)
00406318                  int32_t rax_2371 = ixor(sub(add(bswap(ixor(bswap(ixor(add(bswap(ixor(bswap(sub(bswap(rax_2345), 0x4c2b9f29)), 0xfc100a8d)), 0x9e2ecd4f), 0x38c81765)), 0x858694f9)), 0xd492c8ee), 0x28d582e6), 0x5d1a0250)
004063de                  int32_t rax_2393 = add(add(sub(ixor(add(sub(ixor(ixor(add(anti_symex(sub(rax_2371, 0x3f1295fc), 0xd7d9a944), 0xb29c70af), 0xeecac43f), 0xa064644a), 0xe6d0322a), 0x6da5f208), 0x88b44c3d), 0x17782444), 0x54022fa9), 0xb0fa5f5c)
004064a7                  int32_t rax_2417 = bswap(anti_symex(ixor(sub(bswap(add(bswap(add(sub(add(sub(anti_symex(rax_2393, 0xf0a05ee1), 0x4339e166), 0x8979d078), 0x4a535921), 0xef1933d1)), 0xb9b62339)), 0x44c0ff04), 0xcd9faaec), 0xdaa1b05c))
0040656b                  int32_t rax_2441 = add(bswap(add(sub(add(anti_symex(bswap(add(sub(bswap(sub(bswap(rax_2417), 0x41238aa8)), 0x5e91ddd6), 0x923718c4)), 0x42cb3b1e), 0x74b9c498), 0x2ac3878a), 0x9711386f)), 0xc753a831)
00406634                  int32_t rax_2465 = anti_symex(bswap(bswap(ixor(anti_symex(add(anti_symex(bswap(sub(sub(ixor(anti_symex(rax_2441, 0xc908888a), 0x5c3530ec), 0xf74f9d47), 0xacda0589)), 0x8651ee11), 0xd26a30cd), 0x7bfa4ae5), 0x739e1c9d))), 0x68e5fe5b)
00406687                  int32_t i_9
00406687                  for (i_9 = 3; i_9 s>= 0; i_9 = i_9 - 1)
00406673                      if ((rax_2465 u>> (i_9 << 3).b).b != *(zx.q((arg2 << 2) - i_9 + 3) + &target))
00406673                          break
00406687                  if (i_9 s< 0)
00406675                      goto label_40c8fe
00406675                  rax_251 = 0
00406754              case 0xa
00406754                  int32_t rax_2497 = ixor(sub(sub(add(bswap(sub(sub(anti_symex(sub(anti_symex(ixor(bswap(arg1), 0x3a743415), 0xe558d702), 0xbd21f1a0), 0x9d517191), 0xc828903d), 0xede792c3)), 0x463e8f44), 0xd45fc4f9), 0x7f8ebb0f), 0xcd1a82fb)
00406822                  int32_t rax_2521 = ixor(ixor(anti_symex(add(sub(bswap(anti_symex(ixor(sub(bswap(anti_symex(anti_symex(rax_2497, 0x153c776b), 0x770f26de)), 0xcdc3057f), 0x21eb6926), 0x1e35ae22)), 0xefd6bfef), 0x24bea8a7), 0x3a2b6558), 0x56b08a85), 0xc3668233)
004068e6                  int32_t rax_2545 = add(add(bswap(anti_symex(add(ixor(bswap(ixor(bswap(bswap(add(add(rax_2521, 0xfa05b0a9), 0x85ae8747))), 0x34e7015d)), 0x6e75ec79), 0x73ee6dea), 0x2e7be562)), 0x4bae415e), 0x9c5ca061)
004069aa                  int32_t rax_2569 = sub(anti_symex(anti_symex(sub(sub(bswap(add(add(sub(bswap(bswap(bswap(rax_2545))), 0x7d973282), 0x98023139), 0xea73ee5d)), 0x61386a92), 0x2e5a4971), 0x912618b4), 0x5cd4672b), 0xd3cf0ec2)
00406a7b                  int32_t rax_2595 = add(add(bswap(bswap(bswap(add(bswap(anti_symex(add(anti_symex(anti_symex(sub(bswap(rax_2569), 0xdab83a06), 0x9db8ccf2), 0xb33b3f70), 0x42416731), 0x59ddeda1)), 0x72e09e93)))), 0x9a9ec573), 0x1146c795)
00406b44                  int32_t rax_2619 = ixor(sub(add(anti_symex(anti_symex(ixor(bswap(bswap(add(ixor(bswap(anti_symex(rax_2595, 0x604437fa)), 0x3530c17e), 0x73c1ecb9))), 0xfda7f897), 0x338417d7), 0xd7e22048), 0xa2cb192b), 0x8cb3d3b3), 0x920022f0)
00406c08                  int32_t rax_2643 = ixor(anti_symex(bswap(bswap(bswap(sub(ixor(add(ixor(bswap(add(sub(rax_2619, 0xef4ebe19), 0x3377e59c)), 0x15d00590), 0xc4c1b076), 0xd8af5b43), 0x3a0d3396)))), 0xa546328a), 0x92d2d3b3)
00406cc9                  int32_t rax_2665 = ixor(bswap(sub(ixor(add(anti_symex(anti_symex(anti_symex(sub(anti_symex(sub(rax_2643, 0x33b20dbb), 0x438c4722), 0x400049b5), 0x3198b936), 0x3b805778), 0x4215e6d1), 0x7048cd05), 0xc2f5fe65), 0x1c687de7)), 0x3d10720c)
00406d92                  int32_t rax_2689 = sub(sub(sub(sub(sub(add(ixor(ixor(bswap(bswap(bswap(sub(rax_2665, 0x469cfec0)))), 0xe7a4f6fd), 0x28328019), 0x37952619), 0x9ca2f8e5), 0x33a8d60d), 0xbd4ab564), 0xe933ced1), 0x8423f284)
00406e49                  int32_t rax_2711 = bswap(add(ixor(sub(sub(add(bswap(sub(bswap(sub(sub(rax_2689, 0x8e906f79), 0x4055a771)), 0x143d15b1)), 0x930cc8c2), 0xde1d135d), 0x59a4b7dc), 0xf44fc177), 0x56f941fe))
00406e9c                  int32_t i_10
00406e9c                  for (i_10 = 3; i_10 s>= 0; i_10 = i_10 - 1)
00406e88                      if ((rax_2711 u>> (i_10 << 3).b).b != *(zx.q((arg2 << 2) - i_10 + 3) + &target))
00406e88                          break
00406e9c                  if (i_10 s< 0)
00406e8a                      goto label_40c8fe
00406e8a                  rax_251 = 0
00406f64              case 0xb
00406f64                  int32_t rax_2743 = ixor(anti_symex(bswap(ixor(anti_symex(add(bswap(anti_symex(ixor(add(bswap(sub(arg1, 0x36979d04)), 0xf4d8733e), 0xeea0dcad), 0x62c61ce1)), 0x7f92028d), 0x9a2adc91), 0x3eb0c46e)), 0x66e055e5), 0x64b6076d)
0040702d                  int32_t rax_2767 = sub(add(bswap(bswap(ixor(sub(bswap(ixor(sub(ixor(anti_symex(ixor(rax_2743, 0x83e2676b), 0x561163ce), 0xe7973cde), 0x7a5255e9), 0x4b70658b)), 0xe8e62821), 0x8cf30306))), 0x7ece7a1d), 0x302b3e5f)
004070f1                  int32_t rax_2791 = add(ixor(bswap(add(ixor(ixor(add(bswap(bswap(sub(ixor(bswap(rax_2767), 0xadd83a2f), 0x7c6fb088))), 0x83d79702), 0xc98faa0f), 0xff8b4315), 0xedc51ab1)), 0x33a08f55), 0xd7d561b2)
004071b5                  int32_t rax_2815 = anti_symex(sub(bswap(add(ixor(add(bswap(bswap(bswap(add(sub(ixor(rax_2791, 0x9e524fd3), 0x53bb9112), 0x8045cc76)))), 0xafe6dadb), 0xb66cbf1f), 0x9d66f6b0)), 0xf8180349), 0x352ee36d)
00407283                  int32_t rax_2839 = ixor(add(anti_symex(add(anti_symex(bswap(anti_symex(ixor(anti_symex(bswap(anti_symex(ixor(rax_2815, 0xff9c8d35), 0x668f2822)), 0x2a5ce005), 0x245bb85c), 0xda7edc07)), 0x7e4edd1c), 0x702de2d9), 0xcb77f14e), 0xd429488d), 0x35a36483)
00407351                  int32_t rax_2863 = add(bswap(bswap(anti_symex(sub(anti_symex(ixor(add(sub(add(sub(anti_symex(rax_2839, 0x7edaa3fd), 0xf4e3ac71), 0x27c8372a), 0x748fed83), 0xef9e80da), 0xd5cec302), 0xb07da92b), 0x67098c0d), 0x685897fc))), 0x1337cf54)
00407422                  int32_t rax_2889 = sub(bswap(add(bswap(anti_symex(anti_symex(bswap(bswap(sub(sub(add(bswap(add(rax_2863, 0xac2e3b1d)), 0x785aaa21), 0x6cdb169a), 0x23853038))), 0x3910cba9), 0x5ce0b589)), 0xa5c1b16e)), 0xd150dec6)
004074e6                  int32_t rax_2913 = bswap(sub(sub(bswap(bswap(bswap(add(ixor(ixor(sub(sub(add(rax_2889, 0xd74494db), 0xe1fb85e6), 0x84f2872c), 0xb4b4f458), 0xb5e26eca), 0x458d1ed1)))), 0x6a46288e), 0xc1d956b6))
004075b7                  int32_t rax_2939 = sub(anti_symex(ixor(sub(bswap(ixor(bswap(bswap(sub(bswap(bswap(ixor(add(rax_2913, 0x1b61e9b7), 0x7ab34c15))), 0xac668b29))), 0xedf5c3f3)), 0x8f0de308), 0x7b21bfab), 0xfa5fa43b), 0x47ae1260)
00407661                  int32_t rax_2959 = sub(bswap(add(anti_symex(anti_symex(add(add(bswap(sub(sub(rax_2939, 0xa70c1e60), 0x1787c827)), 0x626b8cfd), 0x89c9412a), 0x975ad376), 0x76d49287), 0x323309b1)), 0xfaf10f69)
004076b4                  int32_t i_11
004076b4                  for (i_11 = 3; i_11 s>= 0; i_11 = i_11 - 1)
004076a0                      if ((rax_2959 u>> (i_11 << 3).b).b != *(zx.q((arg2 << 2) - i_11 + 3) + &target))
004076a0                          break
004076b4                  if (i_11 s< 0)
004076a2                      goto label_40c8fe
004076a2                  rax_251 = 0
00407777              case 0xc
00407777                  int32_t rax_2991 = sub(bswap(add(sub(add(ixor(bswap(ixor(ixor(add(bswap(bswap(arg1)), 0xb63d2200), 0x37bb876f), 0xbc025f9e)), 0xa37c3b5d), 0x172c64bb), 0xa165ec8f), 0xeee13e02)), 0x2231051f)
0040783b                  int32_t rax_3015 = anti_symex(bswap(bswap(ixor(anti_symex(anti_symex(ixor(ixor(bswap(bswap(anti_symex(sub(rax_2991, 0xdceaa1a4), 0x30c588b5))), 0x44d9e3c2), 0x1d25b98f), 0xa32ef5eb), 0x6a006ca7), 0x57a5c315))), 0x73c179a3)
004078fc                  int32_t rax_3037 = bswap(sub(sub(anti_symex(anti_symex(add(ixor(add(ixor(anti_symex(sub(rax_3015, 0x9dbb50a1), 0x13341de7), 0x65095913), 0x9975dcf5), 0x399f5c88), 0xfc71b2c3), 0xf83c46c0), 0x45424a09), 0x60dc4fa1), 0xd2389608))
004079cd                  int32_t rax_3063 = sub(bswap(bswap(add(add(add(bswap(anti_symex(sub(add(bswap(add(bswap(rax_3037), 0x8a1e7114)), 0xc8f90ef0), 0x6263adec), 0x7c645273)), 0xe7219aa8), 0x3ff7a9c7), 0x721f1be6))), 0x122a4de1)
00407a9b                  int32_t rax_3087 = add(bswap(ixor(sub(sub(sub(sub(bswap(sub(add(anti_symex(anti_symex(rax_3063, 0x9d6d7100), 0x5e738404), 0x33993019), 0x73339cad)), 0xc2d39678), 0x1579d786), 0x4e435501), 0x19f1f680), 0x19623457)), 0x4e19b508)
00407b5c                  int32_t rax_3109 = anti_symex(ixor(add(anti_symex(sub(sub(anti_symex(add(anti_symex(ixor(bswap(rax_3087), 0xabd03660), 0x86f04331), 0x4173634a), 0x647904ee), 0xd43545c9), 0x2f180f1a), 0x32f71552), 0x3c74869a), 0x4df62e3a), 0xa3d135e1)
00407c1d                  int32_t rax_3131 = ixor(bswap(ixor(add(anti_symex(add(sub(anti_symex(add(anti_symex(sub(rax_3109, 0xc8f45848), 0x8d826e1f), 0xbba2f853), 0xf11960d3), 0x9a69be92), 0xa440fa54), 0x953f5499), 0xc0cc4205), 0x2b81f70d)), 0x4e3fe3c1)
00407ce4                  int32_t rax_3157 = bswap(ixor(bswap(bswap(ixor(add(bswap(bswap(ixor(ixor(bswap(add(bswap(rax_3131), 0x160b9907)), 0xfeaf6448), 0x2ba44b73))), 0xf628372d), 0x4c92ae46))), 0xd336a461))
00407db2                  int32_t rax_3181 = sub(add(sub(bswap(add(add(sub(anti_symex(bswap(anti_symex(anti_symex(ixor(rax_3157, 0xf841c867), 0xd6a8a3de), 0xf6a26ff9)), 0xc43931a2), 0xc7383b89), 0xf54d29fe), 0xd835cae4)), 0x7f6e9999), 0x28fc91a7), 0x8fd972a0)
00407e73                  int32_t rax_3203 = add(add(ixor(sub(add(add(sub(bswap(ixor(add(ixor(rax_3181, 0xe4158185), 0xe61ea67e), 0x1c035b19)), 0xb3759e46), 0x2a333fcd), 0x4bf66f3d), 0x94fa5be8), 0xd50ca65f), 0x14010279), 0x5dee7ba0)
00407e85                  int32_t rax_3205 = sub(rax_3203, 0x49cdb820)
00407ed8                  int32_t i_12
00407ed8                  for (i_12 = 3; i_12 s>= 0; i_12 = i_12 - 1)
00407ec4                      if ((rax_3205 u>> (i_12 << 3).b).b != *(zx.q((arg2 << 2) - i_12 + 3) + &target))
00407ec4                          break
00407ed8                  if (i_12 s< 0)
00407ec6                      goto label_40c8fe
00407ec6                  rax_251 = 0
00407fa0              case 0xd
00407fa0                  int32_t rax_3237 = add(bswap(anti_symex(anti_symex(bswap(anti_symex(bswap(add(ixor(ixor(anti_symex(anti_symex(arg1, 0x8a94da4a), 0x675a4791), 0xfd3bbbf7), 0x5c7aaa7b), 0x86377df9)), 0xd64efcc3)), 0x83f66417), 0xb0461716)), 0x312e7b7b)
0040806e                  int32_t rax_3261 = sub(ixor(bswap(anti_symex(add(bswap(add(add(anti_symex(anti_symex(add(ixor(rax_3237, 0xf181cad9), 0xb140efb8), 0xa702f0e7), 0xd79013b6), 0xe11777e6), 0xcab12e84)), 0x5db2d301), 0x29ec34ae)), 0xcb77064c), 0x9ac46844)
0040813f                  int32_t rax_3287 = ixor(anti_symex(sub(sub(anti_symex(ixor(bswap(bswap(bswap(add(anti_symex(bswap(bswap(rax_3261)), 0x41bcae6d), 0x93467471)))), 0x269cc83a), 0x7984fbf3), 0x4a02b25d), 0xf8f4c725), 0x780c3b97), 0x31ee18c4)
0040820d                  int32_t rax_3311 = ixor(ixor(bswap(anti_symex(add(ixor(bswap(ixor(anti_symex(anti_symex(add(anti_symex(rax_3287, 0x11cae49d), 0x7d84019d), 0x48deb2dd), 0x4d346e98), 0x3d3f54f6)), 0x6e31a6ec), 0xe36be2cb), 0xdaa38d88)), 0x3f7efeaa), 0x72414f2e)
004082d6                  int32_t rax_3335 = sub(bswap(anti_symex(ixor(bswap(sub(ixor(ixor(sub(bswap(ixor(sub(rax_3311, 0xcf2d3f2b), 0xcdeed5fa)), 0x20143cad), 0xb3a2abd6), 0x1295332e), 0x9ff4eea6)), 0x6308d381), 0x472265c6)), 0x9e91a8cc)
00408397                  int32_t rax_3357 = add(sub(anti_symex(add(add(sub(anti_symex(ixor(sub(anti_symex(bswap(rax_3335), 0xd951d24e), 0xcfcfa1b9), 0x1a9fc967), 0x1da66a9b), 0x2f263b70), 0xe94dfc29), 0xcb941a44), 0x15b30da0), 0x464c4544), 0xa735a53d)
0040845b                  int32_t rax_3381 = ixor(sub(bswap(add(bswap(ixor(sub(sub(bswap(add(anti_symex(bswap(rax_3357), 0x482f42b4), 0xfc2df5d0)), 0xddc9cb0a), 0xeb4da962), 0x7f01c57b)), 0xbbd39cff)), 0xdb536dd4), 0xcb7d64a2)
00408524                  int32_t rax_3405 = bswap(sub(bswap(add(sub(add(bswap(add(sub(add(sub(ixor(rax_3381, 0x48f50223), 0xed761558), 0x250bf4b6), 0x8146f060), 0xf4aa3c51)), 0x50ed57e8), 0x23293abe), 0x88f072f9)), 0x414d76fc))
004085ed                  int32_t rax_3429 = add(add(sub(sub(sub(sub(add(add(bswap(bswap(sub(bswap(rax_3405), 0xcf3409a9))), 0x541d11a3), 0xa4794967), 0xc1090839), 0x429f7673), 0xea1c6690), 0xea131e8b), 0xd0a896c8), 0x8471df0d)
004086a9                  int32_t rax_3451 = add(sub(sub(ixor(sub(ixor(sub(sub(ixor(bswap(bswap(rax_3429)), 0xf6ccb952), 0xa4657249), 0x3f7757d3), 0x9fbf00b7), 0x8d06f888), 0x5636465c), 0x43732304), 0xdccb7d83), 0xcd993a24)
004086fc                  int32_t i_13
004086fc                  for (i_13 = 3; i_13 s>= 0; i_13 = i_13 - 1)
004086e8                      if ((rax_3451 u>> (i_13 << 3).b).b != *(zx.q((arg2 << 2) - i_13 + 3) + &target))
004086e8                          break
004086fc                  if (i_13 s< 0)
004086ea                      goto label_40c8fe
004086ea                  rax_251 = 0
004087c4              case 0xe
004087c4                  int32_t rax_3483 = ixor(ixor(add(add(bswap(bswap(sub(sub(sub(bswap(anti_symex(anti_symex(arg1, 0x4ec26600), 0x63fa4c88)), 0x40f529a2), 0xe654c608), 0x60803ac7))), 0x21516d8f), 0xb3874b2d), 0x16e96164), 0xe6401c17)
00408885                  int32_t rax_3505 = anti_symex(sub(sub(anti_symex(anti_symex(sub(bswap(add(sub(add(ixor(rax_3483, 0xd9caac1f), 0xe4a5257e), 0x95643002), 0x9faf5db3)), 0x93372c6d), 0x3c0cd2c0), 0x998cc015), 0x44880470), 0xd97eefa6), 0xddce9ec2)
00408953                  int32_t rax_3529 = sub(sub(bswap(ixor(bswap(add(sub(add(add(ixor(sub(add(rax_3505, 0x1f9df0aa), 0xe4b0ea57), 0x70684d3b), 0x950b76af), 0x984d01e7), 0x8edcc0a4), 0xa93b10d1)), 0x80e40ebf)), 0xa9d15d74), 0xdb81afd4)
00408a21                  int32_t rax_3553 = anti_symex(add(bswap(anti_symex(sub(anti_symex(ixor(ixor(add(anti_symex(anti_symex(bswap(rax_3529), 0xdb15cfca), 0x828790fc), 0xd0deaffe), 0x938372a2), 0xfdf6be42), 0xe2c5a48c), 0x623d174e), 0x564a9cb6)), 0xa3839799), 0x71a7f78e)
00408ae2                  int32_t rax_3575 = anti_symex(ixor(anti_symex(bswap(sub(ixor(sub(add(sub(add(anti_symex(rax_3553, 0x56968bb0), 0xc4448a26), 0xd71e6ab9), 0xcf20da0a), 0xb5f820d2), 0x93e87def), 0x5a1f4ff9)), 0xb233aca2), 0x1a01d9d6), 0x577011ad)
00408bab                  int32_t rax_3599 = bswap(sub(add(bswap(ixor(add(sub(ixor(bswap(sub(ixor(add(rax_3575, 0x333f626e), 0xae4c8d34), 0xa23aac3b)), 0xafdab1b0), 0xbb694a8b), 0xaf51e2fe), 0x555b79bc)), 0xd6de73c9), 0xb631817d))
00408c74                  int32_t rax_3623 = sub(add(sub(ixor(ixor(add(bswap(add(add(bswap(anti_symex(bswap(rax_3599), 0x9a62f1ae)), 0x7c92ad7e), 0x4e485547)), 0x3e4f9431), 0x7ead61fb), 0xcc481cf2), 0xa4f81c41), 0xe3b98683), 0xe9740d33)
00408d35                  int32_t rax_3645 = add(ixor(add(add(ixor(add(sub(bswap(ixor(add(anti_symex(rax_3623, 0xd2b27868), 0x28cc8d1e), 0xe1412108)), 0x8eb5fd90), 0x8a618c92), 0x4e28dfa7), 0x32e3f553), 0x6407784b), 0x1e2ec3f7), 0x16ba18ce)
00408e03                  int32_t rax_3669 = add(add(ixor(ixor(add(add(bswap(ixor(bswap(sub(ixor(ixor(rax_3645, 0x53771c77), 0x3252e615), 0x23a834a0)), 0xf72a77d8)), 0x998b30ae), 0x4fa5d297), 0xca96bf37), 0xd5281437), 0x4045549e), 0xcc92be76)
00408ec4                  int32_t rax_3691 = ixor(add(add(ixor(add(anti_symex(bswap(anti_symex(anti_symex(anti_symex(sub(rax_3669, 0xc7f2167f), 0xa2d9581b), 0xc213d0ba), 0x3f610c3b)), 0xac23cd7d), 0xfad92b9e), 0xef86cfbc), 0xed0aa895), 0x1e0b3fd2), 0xbc4d0a26)
00408f07                  int32_t rax_3699 = bswap(add(anti_symex(ixor(rax_3691, 0x56e897d5), 0xefc601b9), 0xfc536c4b))
00408f5a                  int32_t i_14
00408f5a                  for (i_14 = 3; i_14 s>= 0; i_14 = i_14 - 1)
00408f46                      if ((rax_3699 u>> (i_14 << 3).b).b != *(zx.q((arg2 << 2) - i_14 + 3) + &target))
00408f46                          break
00408f5a                  if (i_14 s< 0)
00408f48                      goto label_40c8fe
00408f48                  rax_251 = 0
00409022              case 0xf
00409022                  int32_t rax_3731 = ixor(add(sub(sub(add(sub(ixor(bswap(bswap(ixor(bswap(sub(arg1, 0x56626522)), 0xba369f0e))), 0x1a6ec178), 0x3989ee2d), 0xdce31ef9), 0xd3ed427b), 0xa62f26ab), 0x41f80159), 0x4dd46ff3)
004090eb                  int32_t rax_3755 = bswap(add(add(add(anti_symex(add(sub(bswap(sub(sub(bswap(anti_symex(rax_3731, 0xc8b380d7)), 0x7bbe41b2), 0x7ef8a018)), 0x8ebeac52), 0x29126cfc), 0x130972a5), 0x1ce5bbce), 0x1851733c), 0x6080fa16))
004091af                  int32_t rax_3779 = add(bswap(anti_symex(add(sub(bswap(bswap(bswap(ixor(anti_symex(anti_symex(add(rax_3755, 0xcc4edb9c), 0xfb508f67), 0x67cd038a), 0xbc963807)))), 0x32ab4fda), 0xfd86c6a2), 0x5d76089f)), 0x912738f4)
00409278                  int32_t rax_3803 = sub(add(anti_symex(bswap(ixor(bswap(bswap(sub(ixor(add(ixor(ixor(rax_3779, 0x1c6369e2), 0xc661732d), 0x10b7a440), 0xb7ece613), 0x6b878094))), 0x9fce4af9)), 0x93a15c39), 0xed9c388f), 0x2f6ae5a0)
00409341                  int32_t rax_3827 = add(sub(sub(bswap(add(add(bswap(bswap(anti_symex(add(add(ixor(rax_3803, 0x40a3c131), 0xf46e76a1), 0x58bc32a3), 0x6a27ee66))), 0xf37f04f3), 0x6a29c8d9)), 0xf1b44a33), 0xf0155fa7), 0xe0562ee5)
0040940a                  int32_t rax_3851 = add(ixor(ixor(add(ixor(bswap(anti_symex(bswap(bswap(add(sub(add(rax_3827, 0x3e64f36b), 0x358b59a9), 0x7f51bd8a))), 0x11258cf5)), 0xe1efe0ec), 0x845acd3d), 0x15b6095e), 0x6d84d45a), 0x21847dd6)
004094db                  int32_t rax_3877 = add(anti_symex(sub(bswap(bswap(add(anti_symex(bswap(anti_symex(anti_symex(sub(bswap(bswap(rax_3851)), 0x4dcd684e), 0x93cb6e02), 0x63685b04)), 0x719ec741), 0x5a23e9cf))), 0xc67f9aa1), 0x8e54e2cc), 0x7c4b2659)
004095a9                  int32_t rax_3901 = add(ixor(bswap(add(anti_symex(sub(anti_symex(ixor(ixor(sub(ixor(bswap(rax_3877), 0xcb088871), 0x885ae03c), 0xc7c7503f), 0x303e459f), 0x6643bc93), 0xe108afb5), 0x420994df), 0xbefb49c2)), 0x86d050b6), 0xba4c131e)
0040966a                  int32_t rax_3923 = ixor(ixor(sub(bswap(anti_symex(sub(anti_symex(sub(anti_symex(sub(ixor(rax_3901, 0xe83f8f7b), 0x8f2418c0), 0x20bda0e1), 0x71edcf56), 0x3ff58d08), 0x8869bac0), 0xbc3b971f)), 0xbad4f58f), 0x81c45c4e), 0xd39b9151)
00409730                  int32_t rax_3945 = ixor(add(sub(sub(sub(sub(sub(ixor(ixor(ixor(add(rax_3923, 0xa534b1c3), 0x92f8f1d5), 0x8c232e94), 0x35043945), 0x11beb851), 0x2d209565), 0xa8c015b3), 0x34f5dc1c), 0x6efc740c), 0xa2af3d56), 0x9d6ef745)
00409742                  int32_t rax_3947 = anti_symex(rax_3945, 0xadc9890f)
00409795                  int32_t i_15
00409795                  for (i_15 = 3; i_15 s>= 0; i_15 = i_15 - 1)
00409781                      if ((rax_3947 u>> (i_15 << 3).b).b != *(zx.q((arg2 << 2) - i_15 + 3) + &target))
00409781                          break
00409795                  if (i_15 s< 0)
00409783                      goto label_40c8fe
00409783                  rax_251 = 0
00409862              case 0x10
00409862                  int32_t rax_3979 = sub(ixor(bswap(bswap(add(sub(ixor(anti_symex(anti_symex(add(anti_symex(anti_symex(arg1, 0xecd15b50), 0x456ad3d0), 0x9161110b), 0x95173685), 0x25fd48a4), 0xe46dd45d), 0x1ee35840), 0xf6fd7ad0))), 0x967cd521), 0xf03284b8)
00409926                  int32_t rax_4003 = ixor(ixor(add(sub(bswap(add(bswap(add(anti_symex(bswap(add(bswap(rax_3979), 0x51db3dba)), 0x56b05eac), 0x7c6dc8d2)), 0x1dc6a50c)), 0x7ad02c26), 0x3f413cc6), 0x505c1fb8), 0x74f9836d)
004099ec                  int32_t rax_4025 = sub(ixor(sub(sub(add(ixor(anti_symex(add(sub(sub(sub(rax_4003, 0xd3127e15), 0x676f0151), 0x9dc65123), 0x7fc74dd8), 0xdba1af68), 0xa77bf488), 0x2d911a3c), 0x967904a3), 0x512c24bd), 0x803499fb), 0xf9565dba)
00409ab0                  int32_t rax_4049 = anti_symex(anti_symex(bswap(bswap(anti_symex(anti_symex(anti_symex(bswap(anti_symex(anti_symex(sub(bswap(rax_4025), 0x431e4f94), 0x127937a2), 0xef284c1c)), 0x7a53c5e4), 0x620609f2), 0xc076538a))), 0x81f702d2), 0xbcd95398)
00409b7e                  int32_t rax_4073 = sub(bswap(bswap(sub(add(anti_symex(sub(add(ixor(sub(sub(add(rax_4049, 0xb53f8691), 0x82be2947), 0x1007f18b), 0x777726eb), 0x10f48fdc), 0x88c18fcf), 0xc4aebda0), 0xb541290c), 0x5b56bfbd))), 0x1e944984)
00409c3f                  int32_t rax_4095 = add(sub(add(sub(ixor(sub(add(ixor(sub(bswap(ixor(rax_4073, 0xab502060)), 0x2f47fa90), 0x98157c8e), 0x967e42ca), 0x7b8b29d5), 0x14fcf154), 0x2a151acd), 0x81d355e6), 0x13f2ddc2), 0xcae83e3f)
00409d00                  int32_t rax_4117 = sub(add(ixor(anti_symex(add(anti_symex(anti_symex(sub(add(bswap(anti_symex(rax_4095, 0xb82696e2)), 0x84b825b3), 0xec3ddff5), 0xd2663986), 0xc86e18a6), 0xb9d90ac4), 0x210d9949), 0x443336c3), 0x18a5cc6a), 0x9a96d173)
00409dc4                  int32_t rax_4141 = sub(ixor(sub(bswap(bswap(sub(bswap(ixor(anti_symex(bswap(ixor(anti_symex(rax_4117, 0xf94000da), 0x52a81139)), 0xcc7f4ba2), 0xeba4ae77)), 0x71edf127))), 0x992539cd), 0xe38477f2), 0xf7b72029)
00409e92                  int32_t rax_4165 = add(ixor(add(ixor(bswap(sub(sub(ixor(sub(bswap(add(ixor(rax_4141, 0x3fcfafc2), 0xbc9bb19b)), 0xd1f632ad), 0x39e508db), 0x6ecce9a8), 0xcbd8334f)), 0x69f787b9), 0x8265db6d), 0x3dd6d7fb), 0x2457d265)
00409f56                  int32_t rax_4189 = add(ixor(ixor(sub(sub(sub(sub(bswap(bswap(add(bswap(bswap(rax_4165)), 0xa9500bda))), 0xbacbb72c), 0x251a55fb), 0x1a2905d2), 0xdc01cf6b), 0xd0cdaa26), 0xc64ddb7a), 0x16ef2e4e)
00409f7a                  int32_t rax_4193 = sub(sub(rax_4189, 0x5fc8b004), 0x2c6302d2)
00409fcd                  int32_t i_16
00409fcd                  for (i_16 = 3; i_16 s>= 0; i_16 = i_16 - 1)
00409fb9                      if ((rax_4193 u>> (i_16 << 3).b).b != *(zx.q((arg2 << 2) - i_16 + 3) + &target))
00409fb9                          break
00409fcd                  if (i_16 s< 0)
00409fbb                      goto label_40c8fe
00409fbb                  rax_251 = 0
0040a095              case 0x11
0040a095                  int32_t rax_4225 = ixor(add(ixor(ixor(sub(anti_symex(bswap(bswap(bswap(sub(ixor(add(arg1, 0x6304ce69), 0x1c82f56a), 0x9234844c)))), 0xe67e711b), 0x3253a731), 0x3be56a94), 0xb7f35cf3), 0x9a668234), 0x6cc39b01)
0040a15e                  int32_t rax_4249 = ixor(add(ixor(anti_symex(bswap(bswap(sub(bswap(add(add(add(anti_symex(rax_4225, 0x38e752cd), 0x4a52abdf), 0x481e758f), 0x7da71a74)), 0x3aa93a0e))), 0xc30767e0), 0xaa5fd181), 0x783218af), 0x61cdc2bb)
0040a227                  int32_t rax_4273 = anti_symex(add(bswap(add(anti_symex(bswap(anti_symex(ixor(ixor(sub(anti_symex(bswap(rax_4249), 0x64b1ffc4), 0x7c75c1f5), 0xb3644998), 0xaad1b2f6), 0x5980b311)), 0xf40c7a32), 0xee435aef)), 0x6b770935), 0x733f700d)
0040a2f0                  int32_t rax_4297 = anti_symex(anti_symex(sub(bswap(add(ixor(anti_symex(sub(bswap(bswap(ixor(add(rax_4273, 0xa83c9d71), 0xe9efdd76))), 0x181d2aef), 0x79efb14f), 0xa44aa07c), 0xfb887542)), 0x48b7f97e), 0x2ddb1acf), 0x1e61a89d)
0040a3b6                  int32_t rax_4319 = anti_symex(anti_symex(ixor(add(ixor(add(sub(anti_symex(ixor(add(sub(rax_4297, 0x94132986), 0x3e1de216), 0xa2064978), 0xa8954d2d), 0xe1f6682b), 0xcf9c1f60), 0xfc268f70), 0x59699cfc), 0x7e247183), 0x13196dde), 0xabbcbc60)
0040a484                  int32_t rax_4343 = sub(ixor(anti_symex(anti_symex(ixor(anti_symex(ixor(ixor(bswap(add(bswap(anti_symex(rax_4319, 0xde625c14)), 0xef7a1ca4)), 0x880f08e2), 0x4c8f97a6), 0x6958406a), 0xa3cef186), 0x6cf1062e), 0x7a47f0eb), 0xab719b28), 0xd24fce99)
0040a54d                  int32_t rax_4367 = ixor(sub(bswap(bswap(ixor(bswap(sub(ixor(anti_symex(ixor(add(sub(rax_4343, 0x152a6dcf), 0xd30b132d), 0x1fdfe291), 0x5f560020), 0xee5e4969), 0x8c4c0de8)), 0xc8d18d9f))), 0xdbfd4d9f), 0x1c18f974)
0040a61b                  int32_t rax_4391 = add(ixor(anti_symex(bswap(sub(add(sub(bswap(add(add(ixor(add(rax_4367, 0xb54a8746), 0x35e1def0), 0xa1776e32), 0xfd54b0b6)), 0xe3b25430), 0x65b1be09), 0x260ba688)), 0x43d203e8), 0x74be1fa7), 0x1e3ad460)
0040a6e4                  int32_t rax_4415 = ixor(sub(sub(add(bswap(add(ixor(ixor(add(bswap(anti_symex(bswap(rax_4391), 0x979dfca1)), 0x1188d088), 0xfbfa19fe), 0x9e91aa0d), 0xe0b35174)), 0xd406ef2b), 0x69877fc6), 0x50e61789), 0xc7b0b29e)
0040a7ad                  int32_t rax_4439 = add(add(ixor(bswap(bswap(add(add(add(add(ixor(sub(bswap(rax_4415), 0xbf166089), 0xee521f61), 0x31a00a55), 0x80b9d1ef), 0x72db788c), 0xa8daf15d))), 0x539f1cd5), 0xffb68bee), 0x15201e9a)
0040a800                  int32_t i_17
0040a800                  for (i_17 = 3; i_17 s>= 0; i_17 = i_17 - 1)
0040a7ec                      if ((rax_4439 u>> (i_17 << 3).b).b != *(zx.q((arg2 << 2) - i_17 + 3) + &target))
0040a7ec                          break
0040a800                  if (i_17 s< 0)
0040a7ee                      goto label_40c8fe
0040a7ee                  rax_251 = 0
0040a8cd              case 0x12
0040a8cd                  int32_t rax_4471 = sub(anti_symex(sub(sub(anti_symex(ixor(sub(bswap(sub(ixor(ixor(bswap(arg1), 0xf115f332), 0xc0e617e0), 0x786be62d)), 0xbbde2c00), 0x5f33f9a8), 0x64d4b0bf), 0x9c0f94ed), 0x38c3d7ef), 0xc8a63bae), 0x67603ee0)
0040a991                  int32_t rax_4495 = anti_symex(bswap(anti_symex(anti_symex(sub(bswap(bswap(anti_symex(bswap(anti_symex(sub(anti_symex(rax_4471, 0xf9a6ea6d), 0x75e58eac), 0xe40d24cf)), 0x6da01dbf))), 0x90d6d1d8), 0x9395e051), 0xaf07c447)), 0x7885f77e)
0040aa57                  int32_t rax_4517 = anti_symex(ixor(sub(ixor(ixor(anti_symex(add(ixor(ixor(sub(sub(rax_4495, 0xacd960a2), 0x54a60d63), 0x23f6643a), 0x2a366f9f), 0x8cc9e8ca), 0x1f38b491), 0x4393f64b), 0xadec8221), 0xec6ef4eb), 0x29e57ba8), 0xdd3986c0)
0040ab25                  int32_t rax_4541 = ixor(ixor(ixor(add(add(ixor(bswap(bswap(add(anti_symex(ixor(ixor(rax_4517, 0x8f04c18f), 0x57b5fcb3), 0x973fa60e), 0x90efb024))), 0x96f1f97f), 0xf12e955a), 0xf6785b3a), 0x796c3beb), 0x7e609f1c), 0xd2f9ef12)
0040abe9                  int32_t rax_4565 = anti_symex(add(bswap(add(bswap(bswap(bswap(ixor(add(anti_symex(add(ixor(rax_4541, 0xa74cae90), 0xe0f51f17), 0xedfe370a), 0xb298f016), 0xc3be9738)))), 0xf7f9b430)), 0x26afcb29), 0x64ed0eb2)
0040acaf                  int32_t rax_4587 = anti_symex(ixor(anti_symex(anti_symex(anti_symex(ixor(add(anti_symex(anti_symex(ixor(add(rax_4565, 0x28838fc8), 0x4bf7c7cb), 0xa39833b0), 0xc93e35d7), 0x1309495b), 0x20503d13), 0x683887f2), 0xe68d6ff5), 0x5e913eb7), 0x91b3f0f3), 0x43c8ad4e)
0040ad78                  int32_t rax_4611 = ixor(add(bswap(ixor(add(anti_symex(bswap(ixor(sub(ixor(add(bswap(rax_4587), 0x3beaa747), 0xddb7eace), 0x68ee4437), 0x3f93a89b)), 0x24cd2017), 0xb0311e5d), 0x491d9536)), 0x9e0bd83d), 0x34728712)
0040ae3c                  int32_t rax_4635 = sub(bswap(ixor(ixor(bswap(add(add(bswap(bswap(add(ixor(sub(rax_4611, 0xd570e916), 0xb1baa850), 0xf3b56ad4))), 0x56e82648), 0xa90e4cdc)), 0xaabdb711), 0xbba95401)), 0x113b3484)
0040af05                  int32_t rax_4659 = sub(sub(sub(bswap(ixor(ixor(bswap(add(bswap(add(ixor(ixor(rax_4635, 0x86d11c73), 0x4f7d7a9b), 0x81d47258)), 0xc0fb2600)), 0x8938083c), 0x941c1c96)), 0xfa18411d), 0xf1ec129e), 0xf56464d5)
0040afd1                  int32_t rax_4685 = add(ixor(ixor(bswap(ixor(add(bswap(bswap(bswap(bswap(bswap(add(ixor(rax_4659, 0xf1cfb70c), 0xcc76950a)))))), 0x7a20e590), 0xb698e60a)), 0xb5010a92), 0x1ebec408), 0x706b23bd)
0040b024                  int32_t i_18
0040b024                  for (i_18 = 3; i_18 s>= 0; i_18 = i_18 - 1)
0040b010                      if ((rax_4685 u>> (i_18 << 3).b).b != *(zx.q((arg2 << 2) - i_18 + 3) + &target))
0040b010                          break
0040b024                  if (i_18 s< 0)
0040b012                      goto label_40c8fe
0040b012                  rax_251 = 0
0040b0ec              case 0x13
0040b0ec                  int32_t rax_4717 = bswap(ixor(anti_symex(anti_symex(ixor(sub(sub(sub(bswap(add(bswap(ixor(arg1, 0xae8e3b1b)), 0xaf1b9978)), 0x6239c3f1), 0x425d58f0), 0xa5d4c4eb), 0xa446070a), 0xa76fdc89), 0x9fedae69), 0x4bee7af1))
0040b1b0                  int32_t rax_4741 = anti_symex(sub(bswap(anti_symex(bswap(sub(sub(bswap(anti_symex(ixor(add(bswap(rax_4717), 0x383d3cb8), 0x4093157d), 0xff371310)), 0x1b045668), 0x8f295dbc)), 0x74b9ae68)), 0x83acea5d), 0xddda770f)
0040b276                  int32_t rax_4763 = add(anti_symex(ixor(add(sub(anti_symex(anti_symex(ixor(add(ixor(sub(rax_4741, 0x505572e4), 0x4a86308a), 0x486a22f7), 0xc6ae010e), 0xfa124202), 0x86c632b6), 0x625748be), 0xa3ece8d5), 0x7d1506e6), 0x638c51a0), 0x23afed1b)
0040b337                  int32_t rax_4785 = add(anti_symex(anti_symex(anti_symex(anti_symex(add(sub(ixor(anti_symex(add(bswap(rax_4763), 0x85d6acb8), 0xd096475f), 0x2cae5fdb), 0x490f125a), 0x9d0dc8e1), 0xab0c320f), 0x4229badd), 0x61faa69f), 0xcb3c63cc), 0x49a33dbc)
0040b400                  int32_t rax_4809 = ixor(ixor(add(sub(bswap(bswap(anti_symex(anti_symex(sub(bswap(sub(add(rax_4785, 0x889ff677), 0x67b84d35)), 0x8ef49aed), 0xc829ab38), 0x87e00ba4))), 0x9267435f), 0xf6001ccd), 0xb6be3f8b), 0x56b14b28)
0040b4c1                  int32_t rax_4831 = ixor(ixor(add(ixor(ixor(anti_symex(bswap(add(sub(anti_symex(add(rax_4809, 0xc045d27e), 0x344509ca), 0x3e150f19), 0xb7416ef4)), 0x34803f89), 0xc7ed0367), 0xc81e68a4), 0x19f0f417), 0x3f89bf7a), 0xd19f2f55)
0040b587                  int32_t rax_4853 = sub(add(sub(add(sub(anti_symex(add(add(sub(anti_symex(anti_symex(rax_4831, 0xb6707f0f), 0x9e57cdbb), 0x4ccafe97), 0xbfe4084d), 0x7f401a86), 0xa9adc2a9), 0x882188ec), 0x36f3fc2c), 0x35738315), 0x904edaa2), 0x1956e81c)
0040b64b                  int32_t rax_4877 = ixor(ixor(add(add(bswap(bswap(bswap(ixor(bswap(ixor(ixor(add(rax_4853, 0xf7c6cfba), 0xd9c7905b), 0x70c826a6)), 0xfa720bf5)))), 0x3b26d222), 0x3a32edd9), 0xde83d5f8), 0xe24d1282)
0040b70f                  int32_t rax_4901 = sub(ixor(sub(ixor(bswap(ixor(bswap(bswap(ixor(bswap(add(add(rax_4877, 0x22df6dd9), 0x7e5bdc13)), 0xd6075143))), 0x55a80f30)), 0xd41dc3a0), 0x67b550ed), 0x1ec9e80b), 0xf9155e1f)
0040b7db                  int32_t rax_4927 = bswap(ixor(sub(bswap(add(bswap(add(ixor(sub(add(bswap(bswap(bswap(rax_4901))), 0x44d410c6), 0xbb2585c7), 0x9add4c91), 0x414fd283)), 0x4e0b279e)), 0xf9e25ef5), 0x9fe5058f))
0040b7ff                  int32_t rax_4931 = sub(ixor(rax_4927, 0x307cc9b8), 0x52b382d2)
0040b852                  int32_t i_19
0040b852                  for (i_19 = 3; i_19 s>= 0; i_19 = i_19 - 1)
0040b83e                      if ((rax_4931 u>> (i_19 << 3).b).b != *(zx.q((arg2 << 2) - i_19 + 3) + &target))
0040b83e                          break
0040b852                  if (i_19 s< 0)
0040b840                      goto label_40c8fe
0040b840                  rax_251 = 0
0040b91a              case 0x14
0040b91a                  int32_t rax_4963 = ixor(anti_symex(add(bswap(bswap(anti_symex(anti_symex(sub(bswap(add(sub(sub(arg1, 0x8bbd832d), 0x82274fec), 0x78162b62)), 0xcbe1d066), 0xcdcf69c4), 0x8461c287))), 0xc70508fe), 0xe8800704), 0x6a8219cc)
0040b9e3                  int32_t rax_4987 = sub(bswap(anti_symex(ixor(ixor(bswap(sub(ixor(ixor(add(bswap(anti_symex(rax_4963, 0x51d82517)), 0xfdeff155), 0x83d9c98e), 0xebcb668c), 0x9738a8da)), 0xc72dbee2), 0xbd6cd492), 0xce3dd6ec)), 0x40555189)
0040baac                  int32_t rax_5011 = ixor(sub(add(bswap(add(bswap(add(anti_symex(bswap(add(add(ixor(rax_4987, 0x17c49bf1), 0x446c2245), 0xb80656ed)), 0x9abe88db), 0x6b2c6650)), 0xe476f510)), 0x45526536), 0x43370b39), 0xc13679ef)
0040bb7a                  int32_t rax_5035 = ixor(add(anti_symex(ixor(ixor(bswap(anti_symex(anti_symex(sub(ixor(ixor(bswap(rax_5011), 0xe7701252), 0x43ab4ad2), 0xabf06889), 0xe9cf6e02), 0x5a652f5a)), 0x9640eea0), 0xfe120568), 0xb275ad6a), 0xdc1c860d), 0x1017e34e)
0040bc3b                  int32_t rax_5057 = bswap(add(anti_symex(add(add(sub(sub(sub(sub(add(anti_symex(rax_5035, 0xad700cfa), 0x401fe68c), 0x230cc813), 0x55630095), 0x9c1c4e66), 0x3f388b8a), 0x14a89be8), 0x8f355d39), 0x83376cb4), 0xfa167152))
0040bd09                  int32_t rax_5081 = ixor(add(sub(ixor(add(ixor(sub(bswap(anti_symex(anti_symex(anti_symex(bswap(rax_5057), 0x925e0281), 0x9d20be9e), 0x77e1ec7d)), 0x66c8d910), 0x3d8e9c84), 0x2b7f3777), 0xd2a75e27), 0x89569ded), 0xc721e196), 0xc7817689)
0040bdcf                  int32_t rax_5103 = ixor(anti_symex(anti_symex(anti_symex(sub(anti_symex(sub(ixor(add(add(anti_symex(rax_5081, 0x1498a23b), 0x3df00e38), 0x9e03b96b), 0x7dddb60e), 0x320bfc9d), 0x3fc23646), 0x39b419a6), 0xa1ee3b4a), 0x5dc3d4b3), 0x7fb46222), 0x6083943f)
0040be93                  int32_t rax_5127 = bswap(sub(bswap(ixor(add(add(ixor(bswap(add(sub(bswap(anti_symex(rax_5103, 0xe14bc499)), 0x1dd93f28), 0xe60fb422)), 0xa0c554b6), 0x90941993), 0x6576ae26), 0x58183dc1)), 0x49584cc2))
0040bf61                  int32_t rax_5151 = ixor(bswap(ixor(sub(add(ixor(add(add(bswap(add(sub(add(rax_5127, 0x92d58a31), 0x2378a262), 0xb76edc45)), 0x94a705d5), 0xb13242b7), 0xeee0b889), 0xd3672a82), 0x7243e08f), 0xda9b9702)), 0xee7cc056)
0040c027                  int32_t rax_5173 = add(ixor(sub(sub(ixor(add(add(add(add(add(sub(rax_5151, 0x3e37cff9), 0x16781df7), 0x117cbac8), 0xe69b4969), 0x72b90f5a), 0x97639dfd), 0x9d64467d), 0x5f8f8226), 0xf3de037c), 0x1173159d), 0x1e23538d)
0040c04b                  int32_t rax_5177 = ixor(add(rax_5173, 0xf1c7c8b4), 0xb6e64bfc)
0040c09e                  int32_t i_20
0040c09e                  for (i_20 = 3; i_20 s>= 0; i_20 = i_20 - 1)
0040c08a                      if ((rax_5177 u>> (i_20 << 3).b).b != *(zx.q((arg2 << 2) - i_20 + 3) + &target))
0040c08a                          break
0040c09e                  if (i_20 s< 0)
0040c08c                      goto label_40c8fe
0040c08c                  rax_251 = 0
0040c15e              case 0x15
0040c15e                  int32_t rax_5207 = sub(anti_symex(ixor(sub(bswap(add(ixor(add(sub(ixor(sub(arg1, 0xbbf95657), 0x2951ae44), 0x6377d9c0), 0x1083510a), 0x375600fb), 0x11e9e2e2)), 0x753dc5df), 0xeb86870e), 0x39897090), 0x2dc1432c)
0040c22c                  int32_t rax_5231 = add(sub(add(anti_symex(ixor(ixor(bswap(ixor(bswap(ixor(add(sub(rax_5207, 0x3d1e81b3), 0x24c9e9ef), 0x40555ecf)), 0x3c55c322)), 0xeb467104), 0x9208728f), 0xb95f0dd2), 0x280424ec), 0x19871c0a), 0xac98057a)
0040c2fa                  int32_t rax_5255 = sub(ixor(bswap(anti_symex(bswap(anti_symex(sub(anti_symex(ixor(ixor(ixor(add(rax_5231, 0x2ed68423), 0xf8fe769a), 0xd1659d0f), 0x4bcb9b7b), 0xc1d21d7f), 0x2633e33f), 0xb92d79a0)), 0x71052ea7)), 0x539fc638), 0x2ce86199)
0040c3bb                  int32_t rax_5277 = anti_symex(anti_symex(ixor(bswap(sub(anti_symex(sub(ixor(sub(add(sub(rax_5255, 0x9d399257), 0x970bfb7a), 0x8ba9cc34), 0xf207d717), 0xdf095de7), 0x18b5b28d), 0x1e4a0597)), 0xcd3f1e9c), 0x4f8e593b), 0xbe532fe0)
0040c47c                  int32_t rax_5299 = add(sub(sub(anti_symex(add(add(ixor(anti_symex(bswap(sub(add(rax_5277, 0x4690e625), 0x52843520)), 0x3960c670), 0xdeb82da9), 0x5f9e925a), 0x27170a8c), 0x26da6839), 0x8ba370d8), 0x28a57392), 0xca97b372)
0040c54a                  int32_t rax_5323 = ixor(sub(anti_symex(bswap(add(add(bswap(add(anti_symex(ixor(ixor(ixor(rax_5299, 0xcddbe896), 0x95964d00), 0xc92e7e74), 0xa94a4645), 0x42f45807)), 0x4a75465c), 0x1e1e0f19)), 0x141423e3), 0xf4198acf), 0xeabf574c)
0040c618                  int32_t rax_5347 = anti_symex(ixor(bswap(anti_symex(bswap(anti_symex(ixor(add(anti_symex(add(sub(ixor(rax_5323, 0xf544dc58), 0xee91b176), 0x8c2d45a2), 0x8dfec5d7), 0x1186c924), 0xe004bf1c), 0x6f2646bf)), 0xf9b8fd26)), 0xea02aa9a), 0x2c073f3f)
0040c6de                  int32_t rax_5369 = sub(ixor(ixor(ixor(add(sub(sub(add(anti_symex(sub(sub(rax_5347, 0x15d78e03), 0xb5682930), 0x87c8f217), 0x12a93e6c), 0x8bd71b49), 0x106bbabf), 0x1b0150e9), 0xf68fb849), 0x84ce296c), 0x205210a5), 0x2f2c3ac3)
0040c79f                  int32_t rax_5391 = add(add(anti_symex(ixor(add(bswap(anti_symex(sub(add(sub(anti_symex(rax_5369, 0xf6181566), 0xe55be5be), 0xdc79feed), 0xc12dd3be), 0x9a5ce507)), 0x9dde90f8), 0xab970fdc), 0x1148823e), 0x5628ab71), 0x6414fb34)
0040c86d                  int32_t rax_5415 = ixor(sub(add(ixor(ixor(bswap(sub(ixor(bswap(ixor(ixor(ixor(rax_5391, 0xd0d1a17c), 0x93aadb42), 0x26ed0bc7)), 0xe067ef85), 0xccd48d4b)), 0x41e4912f), 0x950ba80c), 0x17c203ca), 0xf9932541), 0x53984823)
0040c8ab                  int32_t rax_5423 = ixor(bswap(add(bswap(rax_5415), 0xc73f4003)), 0xb6bf4a18)
0040c8fb                  int32_t i_21
0040c8fb                  for (i_21 = 3; i_21 s>= 0; i_21 = i_21 - 1)
0040c8ea                      if ((rax_5423 u>> (i_21 << 3).b).b != *(zx.q((arg2 << 2) - i_21 + 3) + &target))
0040c8ea                          break
0040c8fb                  if (i_21 s< 0)
0040c8ec                      goto label_40c8fe
0040c8ec                  rax_251 = 0
0040c904      return rax_251
```

anti_symex

```
0040145c      int32_t rcx_4 = ((not.d(arg1) & arg2) << 2) - (arg1 ^ arg2) - (arg1 | arg2) + (not.d(arg1 | arg2) << 2) + (arg1 ^ arg2) + arg2 - (not.d(arg2) | arg1) + arg1 * 6 + not.d(arg2) * 5 - (arg1 ^ arg2) - (arg1 | arg2) - not.d(arg1) * 2 - (not.d(arg1 | arg2) << 2) - ((not.d(arg2) & arg1) << 2)
0040147a      return zx.q((not.d(arg1) & arg2) * 3 + rcx_4 + 2)
```

 - 중요한 코드의 내용들은 다음과 같다.

## recv

```
 for (int32_t i = 0; i u<= 0x15; i = i + 1)
0040ccbe          int32_t rdx_5 = sx.d(*(&var_d8 + zx.q(i << 2))) << 0x18 | sx.d(*(&var_d8 + zx.q((i << 2) + 1))) << 0x10 | sx.d(*(&var_d8 + zx.q((i << 2) + 2))) << 8
0040ccf8          if (chall(sx.d(*(&var_d8 + zx.q(i << 2 | 3))) | rdx_5, i) == 0)
0040cd20              send(fd: fd_1, buf: buf_2, len: strlen(buf_2), flags: 0)
0040cd2a              sleep(seconds: 1)
0040cd37              close(fd: fd_1)
```
 - main 에서 코드를보면 input값으로 받은값을 4바이트씩 끊어서 인자로 chall에 반복문의 index와 함께 넘기고있다.
 - chall 로 넘긴값들은 각종 연산을통해 암호화되며 중요한부분이 anti_symex라는 부분인데
```
0040145c      int32_t rcx_4 = ((not.d(arg1) & arg2) << 2) - (arg1 ^ arg2) - (arg1 | arg2) + (not.d(arg1 | arg2) << 2) + (arg1 ^ arg2) + arg2 - (not.d(arg2) | arg1) + arg1 * 6 + not.d(arg2) * 5 - (arg1 ^ arg2) - (arg1 | arg2) - not.d(arg1) * 2 - (not.d(arg1 | arg2) << 2) - ((not.d(arg2) & arg1) << 2)
0040147a      return zx.q((not.d(arg1) & arg2) * 3 + rcx_4 + 2)
```
 - 내용은 이렇다 학술적인 용어가 기억이나지않아 서술하지못한다
 - 다만 이 수식은 결국 매개변수 + 매개변수2 이다
 - symbolic execution을 방지하기위한 차원에서 만들어 놓은 코드인것같다.

```
for (i = 3; i s>= 0; i = i - 1)
00401cce                      if ((rax_242 u>> (i << 3).b).b != *(zx.q((arg2 << 2) - i + 3) + &target))
00401cce                          break
00401ce2                  if (i s< 0)
00401cd0                      goto label_40c8fe
```
 - 연산을 끝난후 해당 조건식으로 전역변수에 저장되어있는 값들과 비교하게된다.
 - 맞을경우 break 틀릴경우 goto label_40c8fe 로 가게된다.
 - 그러면 explore 로 find를 수식연산이 끝나는 지점에서 담기는 변수의 값을 분석하여 자동화하고 aviod로 goto 로 못가게 하면된다.

exploit
```
import angr
import unicorn
import claripy
from pwn import *
from unicorn.x86_const import *

BASE_ADDR = 0x400000 

def CASE_1(proj, args,state,inputs,i):
    block = proj.factory.block(BASE_ADDR+0x14bb)
    state.regs.rip = BASE_ADDR + 0x14bb
    simgr = proj.factory.simgr(state)
    for input_byte in inputs:
        state.solver.add(input_byte > 0x20) 
        state.solver.add(input_byte <= 0x7e)

    input_4 = claripy.Concat(inputs[i],inputs[i+1],inputs[i+2],inputs[i+3])

    for insn in block.capstone.insns:
        print(f'addr : {insn}')
        if insn.op_str[5:9] == 'eax':
            state.regs.eax = input_4
            print(f'call func: {state.regs.eax}')
            print(f'rip : {state.regs.rip}')
    
    simgr.explore(find = 0x401C8F, aviod=0x402510)
    if simgr.found:
        sol_state = simgr.found[0]
        print("sol found")
        print(f'eax : {sol_state.regs.eax}')
        print(sol_state.solver.eval(input_4))

def main(args):
    project = angr.Project(args.binary, main_opts={'base_addr': BASE_ADDR})
    state = project.factory.blank_state()
    inputs = [claripy.BVS('input_%d' % i, 8) for i in range(88)]
    for i in range(22):
        CASE_1(project,args,state,inputs,i)
        print(f'i : {i}')
    


if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("binary")
    args = parser.parse_args()
    main(args)
```
   
