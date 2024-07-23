import {
  AllowListData,
  PublicDrop,
  SignedMintValidationParams,
  TokenGatedDropStage
pragma solidity 0.8.17;

pragma solidity ^0.4.21;

function addBalance(address balanceHolder, uint amount) internal {
    setBalance(balanceHolder, getBalance(balanceHolder) + amount);
pragma solidity 0.8.17;

