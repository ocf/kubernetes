{ pkgs, lib, config, inputs, ... }:

{
  packages = with pkgs; [ 
    git
    teleport
    k9s
    kubectl
    inputs.transpire.packages.${pkgs.system}.default
  ];
}
