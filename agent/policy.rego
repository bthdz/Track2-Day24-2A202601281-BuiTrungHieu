package agent.policy

# Default policy decisions
default allow = false

# Rule: Block egress of restricted data (Lethal trifecta containment)
deny {
    input.data_classification == "restricted"
    input.egress_enabled == true
}

allow {
    not deny
}

reason = "Restricted data egress is strictly forbidden by policy" {
    deny
}

reason = sprintf("Policy check passed for data_classification='%s', egress_enabled=%v", [input.data_classification, input.egress_enabled]) {
    allow
}
