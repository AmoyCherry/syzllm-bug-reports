## 1. Kernel
### Download Linux 6.16-rc3

```bash
wget https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/snapshot/linux-6.16-rc3.tar.gz
```

### Generate default configs

```
cd $KERNEL
make defconfig
make kvm_guest.config
```

### Enable .confg

Clear auto-generated content by using `:%d` in vim.

Then copy and paste my [.config](https://github.com/AmoyCherry/syzllm-bug-reports/blob/main/bugs/6.16rc3/.config) content.

At last call the command `make olddefconfig`.

### Build the kernel 

```bash
make -j`nproc`
```

## 2. Root File System

### Install debootstrap

```
sudo apt install debootstrap
```

### Create Debian Bullseye Linux image

Create a Debian Bullseye Linux image with the minimal set of required packages.

```
mkdir image
cd image
wget https://raw.githubusercontent.com/google/syzkaller/master/tools/create-image.sh -O create-image.sh
chmod +x create-image.sh
./create-image.sh
```

> You might want to check how exactly this image was built. Check with the [script](https://raw.githubusercontent.com/google/syzkaller/master/tools/create-image.sh).

The result should be `image/bullseye.img` disk image.

## 3. Run repro.c

Remember to replace `$KERNEL` and `$IMAGE` with your own paths.

```bash
sudo qemu-system-x86_64 -m 4G -smp 4 -kernel $KERNEL/arch/x86/boot/bzImage -append "console=ttyS0 root=/dev/sda earlyprintk=serial net.ifnames=0" -drive file=$IMAGE/bullseye.img,format=raw -net user,host=10.0.2.10,hostfwd=tcp:127.0.0.1:10021-:22 -net nic,model=e1000 -enable-kvm -nographic -pidfile vm.pid 2>&1 | tee vm.log
```

