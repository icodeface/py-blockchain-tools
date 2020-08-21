#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os

VERSION = '101'
LOCAL_IP = '172.18.1.1'
LOTUS_P2P_LISTEN = 1234
LOTUS_ANNOUNCED = f"""["/ip4/{LOCAL_IP}/tcp/{LOTUS_P2P_LISTEN}"]"""

MINER_P2P_LISTEN = 1235
MINER_ANNOUNCED = f"""["/ip4/1.2.3.4/tcp/49512", "/ip4/5.6.7.8/tcp/49512"]"""

DATA_PATH = '~/share/ssd/data'
SCRIPT_PATH = '~/share/ssd/script'


def replace_file(filename, s, print_f=True):
    with open(os.path.join(SCRIPT_PATH, filename), "w+") as f:
        f.seek(0)
        f.truncate()
        f.write(s)

    if print_f:
        with open(os.path.join(SCRIPT_PATH, filename), "r") as f:
            print(f.read())
            print('-' * 80)
            print('-' * 80)
    print(f"[*] write {filename} done")


def gen_run_lotus():
    s = f"""#!/bin/bash
set -e

S=star
V={VERSION}

sleep 10

export RUST_BACKTRACE=full
export RUSTFLAGS="-C target-cpu=native -g"
export FFI_BUILD_FROM_SOURCE=1
export RUST_LOG=info

export LOTUS_PATH="/home/ps/share/ssd/data/lotus_$V"

export IPFS_GATEWAY="https://proof-parameters.s3.cn-south-1.jdcloud-oss.com/ipfs/"
export FIL_PROOFS_PARAMETER_CACHE="/home/ps/share/ssd/data/filecoin-proof-parameters"

unset FIL_PROOFS_MAXIMIZE_CACHING
export SKIP_BASE_EXP_CACHE=1

export GOLOG_LOG_FMT=json

mkdir -p /home/ps/share/ssd/bin/bin_$V/
cp /home/ps/share/ssd/bin/bin_$S/lotus /home/ps/share/ssd/bin/bin_$V/
/home/ps/share/ssd/bin/bin_$V/lotus daemon &
sudo prlimit --nofile=1048576 --nproc=unlimited --rtprio=99 --nice=-19 --pid $!

wait
    """
    filename = os.path.join(SCRIPT_PATH, f"run_lotus_{VERSION}.sh")
    replace_file(filename, s)
    os.system(f"chmod +x {filename}")


def lotus_superv_conf():
    s = f"""[program:lotus_{VERSION}]
command=/home/ps/share/ssd/script/run_lotus_{VERSION}.sh
user=ps

autostart=true
autorestart=true
stopwaitsecs=60
startretries=100
stopasgroup=true
killasgroup=true

redirect_stderr=true
stdout_logfile=/home/ps/share/hdd/log/lotus_{VERSION}.log
"""
    filename = "/etc/supervisor/conf.d/lotus.conf"
    replace_file(filename, s)


def update_lotus_config():
    s = f"""# Default config:
[API]
ListenAddress = "/ip4/{LOCAL_IP}/tcp/1819/http"
#  RemoteListenAddress = ""
#  Timeout = "30s"
#
[Libp2p]
ListenAddresses = ["/ip4/0.0.0.0/tcp/{LOTUS_P2P_LISTEN}"]
AnnounceAddresses = {LOTUS_ANNOUNCED}
#  NoAnnounceAddresses = []
ConnMgrLow = 896
ConnMgrHigh = 1024
#  ConnMgrGrace = "20s"
#
[Pubsub]
#  Bootstrapper = false
#  RemoteTracer = "/ip4/147.75.67.199/tcp/4001/p2p/QmTd6UvR47vUidRNZ1ZKXHrAFhqTJAD27rKL9XYghEKgKX"
#
[Client]
#  UseIpfs = false
#  IpfsMAddr = ""
#  IpfsUseForRetrieval = false
#
[Metrics]
#  Nickname = ""
#  HeadNotifs = false
#
    """
    replace_file(os.path.join(DATA_PATH, f"lotus_{VERSION}/config.toml"), s)


def update_lotus_api():
    dest = os.path.join(DATA_PATH, 'lotus')
    if not os.path.exists(dest):
        os.mkdir(dest)
    os.system(f"cp {os.path.join(DATA_PATH, 'lotus_{}/api'.format(VERSION))} {dest}")
    os.system(f"cp {os.path.join(DATA_PATH, 'lotus_{}/token'.format(VERSION))} {dest}")


def gen_init_miner():
    worker = input("worker address:")
    s = f"""#!/bin/bash
S=star
V={VERSION}
O={worker}

export RUST_BACKTRACE=full
export RUSTFLAGS="-C target-cpu=native -g"
export FFI_BUILD_FROM_SOURCE=1
export RUST_LOG=trace

export LOTUS_PATH="/home/ps/share/ssd/data/lotus_$V"
export LOTUS_MINER_PATH="/home/ps/share/ssd/data/lotusminer_$V"

export IPFS_GATEWAY="https://proof-parameters.s3.cn-south-1.jdcloud-oss.com/ipfs/"
export FIL_PROOFS_PARAMETER_CACHE="/home/ps/share/ssd/data/filecoin-proof-parameters"

unset FIL_PROOFS_MAXIMIZE_CACHING
export SKIP_BASE_EXP_CACHE=1

export GOLOG_LOG_FMT=json

mkdir -p /home/ps/share/ssd/bin/bin_$V
cp /home/ps/share/ssd/bin/bin_$S/lotus-miner /home/ps/share/ssd/bin/bin_$V/
/home/ps/share/ssd/bin/bin_$V/lotus-miner init --owner=$O --sector-size=32GiB
    """
    filename = os.path.join(SCRIPT_PATH, f'init_miner_{VERSION}.sh')
    replace_file(filename, s)
    os.system(f"chmod +x {filename}")


def update_miner_config():
    s = f"""# Default config:
[API]
ListenAddress = "/ip4/{LOCAL_IP}/tcp/2819/http"
RemoteListenAddress = "{LOCAL_IP}:2819"
#  Timeout = "30s"
#
[Libp2p]
ListenAddresses = ["/ip4/0.0.0.0/tcp/{MINER_P2P_LISTEN}"]
AnnounceAddresses = {MINER_ANNOUNCED}
#  NoAnnounceAddresses = []
ConnMgrLow = 896
ConnMgrHigh = 1024
#  ConnMgrGrace = "20s"
#
[Pubsub]
#  Bootstrapper = false
#  RemoteTracer = "/ip4/147.75.67.199/tcp/4001/p2p/QmTd6UvR47vUidRNZ1ZKXHrAFhqTJAD27rKL9XYghEKgKX"
#
[Dealmaking]
#  ConsiderOnlineStorageDeals = true
#  ConsiderOfflineStorageDeals = true
#  ConsiderOnlineRetrievalDeals = true
#  ConsiderOfflineRetrievalDeals = true
#  PieceCidBlocklist = []
#  ExpectedSealDuration = "1m0s"
#  Filter = ""
#
[Sealing]
#  MaxWaitDealsSectors = 2
#  MaxSealingSectors = 0
#  MaxSealingSectorsForDeals = 0
#  WaitDealsDelay = "1m0s"
#
[Storage]
ParallelSealLimit = 21
ParallelFetchLimit = 100
LargeMemoryMode = true
FetchToShared = true
#  AllowAddPiece = false
#  AllowPreCommit1 = false
#  AllowPreCommit2 = false
#  AllowCommit = false
#  AllowUnseal = false
#
[Fees]
#  MaxPreCommitGasFee = "0.05 FIL"
#  MaxCommitGasFee = "0.05 FIL"
#  MaxWindowPoStGasFee = "50 FIL"
#
"""
    replace_file(os.path.join(DATA_PATH, f"lotusminer_{VERSION}/config.toml"), s)


def gen_run_miner():
    s = f"""#!/bin/bash
set -e

S=star
V={VERSION}

sleep 10

WORK_PATH=$(dirname $0)
$WORK_PATH/mount_hdd.sh

export RUST_BACKTRACE=full
export RUSTFLAGS="-C target-cpu=native -g"
export FFI_BUILD_FROM_SOURCE=1
export RUST_LOG=info

export LOTUS_PATH="/home/ps/share/ssd/data/lotus_$V"
export LOTUS_MINER_PATH="/home/ps/share/ssd/data/lotusminer_$V"

export IPFS_GATEWAY="https://proof-parameters.s3.cn-south-1.jdcloud-oss.com/ipfs/"
export FIL_PROOFS_PARAMETER_CACHE="/home/ps/share/ssd/data/filecoin-proof-parameters"

export FIL_PROOFS_MAXIMIZE_CACHING=1
export SKIP_BASE_EXP_CACHE=1

export GOLOG_LOG_FMT=json

mkdir -p /home/ps/share/ssd/bin/bin_$V
cp /home/ps/share/ssd/bin/bin_$S/lotus-miner /home/ps/share/ssd/bin/bin_$V/
/home/ps/share/ssd/bin/bin_$V/lotus-miner run &
sudo prlimit --nofile=1048576 --nproc=unlimited --rtprio=99 --nice=-19 --pid $!

wait
"""
    filename = os.path.join(SCRIPT_PATH, f'run_miner_{VERSION}.sh')
    replace_file(filename, s)
    os.system(f"chmod +x {filename}")


def update_miner_api():
    dest = os.path.join(DATA_PATH, 'lotusminer')
    if not os.path.exists(dest):
        os.mkdir(dest)
    os.system(f"cp {os.path.join(DATA_PATH, 'lotusminer_{}/api'.format(VERSION))} {dest}")
    os.system(f"cp {os.path.join(DATA_PATH, 'lotusminer_{}/token'.format(VERSION))} {dest}")


def gen_mount_hdd():
    old = os.path.join(SCRIPT_PATH, "mount.sh")
    if os.path.exists(old):
        os.unlink(old)
    os.chdir("/home/ps/share/ssd/script/fabric/fabric_storage")
    os.system("fab shell")
    with open(old, 'r') as f:
        text = f.read()
        s = f"""#!/bin/bash
R=()

{text}

for I in ${{R[@]}}
do
  wait $I
  J=$?
  [ $J -ne 0 ] && exit 1
done
exit 0
"""
        filename = os.path.join(SCRIPT_PATH, "mount_hdd.sh")
        replace_file(filename, s, False)
        os.system(f"chmod +x {filename}")


def miner_superv_conf():
    s = f"""[program:miner_{VERSION}]
command=/home/ps/share/ssd/script/run_miner_{VERSION}.sh
user=ps

autostart=true
autorestart=true
stopwaitsecs=60
startretries=100
stopasgroup=true
killasgroup=true

redirect_stderr=true
stdout_logfile=/home/ps/share/hdd/log/miner_{VERSION}.log
"""

    filename = "/etc/supervisor/conf.d/miner.conf"
    replace_file(filename, s)


def gen_run_worker():
    s = f"""#!/bin/bash
set -e

V={VERSION}
IP={LOCAL_IP}

[ $(mount -l | grep /home/ps/share | wc -l) -eq 1 ] || ( mkdir -p /home/ps/share && sudo mount -t nfs -o hard,intr,bg,nofail,noatime ${{IP}}:/home/ps/share /home/ps/share && sudo chown ps.ps /home/ps/share )

/home/ps/share/ssd/script/mount_hdd.sh

/home/ps/share/ssd/script/run_worker_$V.sh
    """

    filename = os.path.join(SCRIPT_PATH, "run_worker.sh")
    replace_file(filename, s)
    os.system(f"chmod +x {filename}")

    s = """#!/bin/bash
set -e

S=star

sleep 10

export RUST_BACKTRACE=full
export RUST_LOG=trace

export LOTUS_PATH="/home/ps/share/ssd/data/lotus"
export LOTUS_MINER_PATH="/home/ps/share/ssd/data/lotusminer"
export WORKER_PATH="/mnt/md0/lotusworker"

export IPFS_GATEWAY="https://proof-parameters.s3.cn-south-1.jdcloud-oss.com/ipfs/"
export FIL_PROOFS_PARAMETER_CACHE="/mnt/md0/filecoin-proof-parameters"

export FIL_PROOFS_MAXIMIZE_CACHING=1
unset USE_EXP_CACHE
export FIL_PROOFS_USE_GPU_COLUMN_BUILDER=1
export FIL_PROOFS_USE_GPU_TREE_BUILDER=1

export GOLOG_LOG_FMT=json

IP=`hostname -I | awk '{print $1}'`

nvidia-smi
if [ $? -ne 0 ]; then
  echo "ERROR: no GPU detected $IP"
  exit
fi

mkdir -p /home/ps/data
cp /home/ps/share/ssd/bin/bin_$S/lotus-worker /home/ps/data/
/home/ps/data/lotus-worker run --listen ${IP}:3456 --parallel-fetch-limit 8 >> /home/ps/share/hdd/log/worker.${IP}.log 2>&1 &
sudo prlimit --nofile=1048576 --nproc=unlimited --rtprio=99 --nice=-19 --pid $!

wait
    """

    filename = os.path.join(SCRIPT_PATH, f"run_worker_{VERSION}.sh")
    replace_file(filename, s)
    os.system(f"chmod +x {filename}")


def gen_worker_conf():
    s = """[program:worker]
command=/home/ps/data/run_worker.sh
user=ps

autostart=true
autorestart=true
stopwaitsecs=60
startretries=100
stopasgroup=true
killasgroup=true

redirect_stderr=true
stdout_logfile=/home/ps/worker.log
    """
    dest = '/home/ps/share/ssd/conf/'
    if not os.path.exists(dest):
        os.mkdir(dest)
    replace_file(os.path.join(dest, "worker.conf"), s)


if __name__ == "__main__":
    cmds = {
        "gen-run-lotus": gen_run_lotus,
        "lotus-superv-conf": lotus_superv_conf,
        "update-lotus-config": update_lotus_config,
        "update-lotus-api": update_lotus_api,
        "gen-init-miner": gen_init_miner,
        "update-miner-config": update_miner_config,
        "gen-mount-hdd": gen_mount_hdd,
        "gen-run-miner": gen_run_miner,
        "miner-superv-conf": miner_superv_conf,
        "update-miner-api": update_miner_api,
        "gen-run-worker": gen_run_worker,
        "gen-worker-conf": gen_worker_conf,
    }

    argv = sys.argv[1:]
    assert(len(argv) == 1)
    cmds[argv[0]]()
