package baywalk.network

default allow = false
allow {
  input.encryption.at_rest == true
  input.encryption.in_transit == true
  input.rbac.ok == true
  input.zones.valid == true
}
