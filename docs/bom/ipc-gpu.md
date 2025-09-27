# IPC + GPU Bill of Materials (Sample)

| Item | Part Number | Qty | Unit Cost (USD) | Est. Watts | PoE Class |
| --- | --- | ---: | ---: | ---: | --- |
| Camera, 2.8mm fixed dome | CAM-2.8MM | 16 | 350 | 12 | 3 |
| IPC with discrete GPU | IPC-GPU | 1 | 1500 | 200 | N/A |
| PoE+ Switch 48-port | POE48 | 1 | 2200 | 120 | N/A |
| NVMe SSD 2TB | SSD-2TB | 2 | 120 | 5 | N/A |
| Rack UPS 2200VA | UPS-2200VA | 1 | 650 | N/A | N/A |
| Camera mounts kit | MOUNTS | 16 | 25 | N/A | N/A |
| NEMA enclosure | ENCLOSURES | 2 | 75 | N/A | N/A |
| Cat6A bulk cable (100m) | CABLING-100M | 2 | 80 | N/A | N/A |
| Labels pack | LABELS | 1 | 30 | N/A | N/A |
| Patch panel + keystones | PATCH-24P | 1 | 100 | N/A | N/A |

Approximate subtotal: $15130

Notes:
- Per-camera PoE draw estimated at 12W (Class 3). Budget for IR/varifocal if used.
- IPC thermals assume 300W PSU with 30% headroom.
- Use 48-port to avoid oversubscription at 16+ cameras.
