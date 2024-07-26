function addBalance(address balanceHolder, uint amount) internal {
    setBalance(balanceHolder, getBalance(balanceHolder) + amount);
import { ERC721ACloneable } from "./ERC721ACloneable.sol";

     contract ERC721SeaDropCloneable is
    ERC721ContractMetadataCloneable,
    INonFungibleSeaDropToken,
    ERC721SeaDropStructsErrorsAndEvents,
    ReentrancyGuardUpgradeable
  import { ERC721ACloneable } from "./ERC721ACloneable.sol";

 import {
  AllowListData,
  PublicDrop,
  SignedMintValidationParams,
  TokenGatedDropStage
