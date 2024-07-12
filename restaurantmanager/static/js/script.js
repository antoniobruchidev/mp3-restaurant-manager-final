  /**function to check if metamask in installed */
const checkInstalled = () => {
  if (typeof window.ethereum == 'undefined') {
    return false;
  } else {
    $('#metamask').on('click', connectWithMetamask);
    return true;
  }
}

/** Function to connect to metamask */
const connectWithMetamask = async () => {
  // A Web3Provider wraps a standard Web3 provider, which is
  // what MetaMask injects as window.ethereum into each page
  window.provider = new ethers.providers.Web3Provider(window.ethereum);
  // MetaMask requires requesting permission to connect users accounts
  const accounts = await provider.send("eth_requestAccounts", []);
  const address =  await accounts[0];

  // The MetaMask plugin also allows signing transactions to
  // send ether and pay to change state within the blockchain.
  // For this, you need the account signer...
  const signer = provider.getSigner()

  $('#web3_address').val(address);
  $('#mnemonic').val("EOA");
  $('#priv').val("EOA");
  $('#submit').click();

  return true;
}

  /**
 * Function to handle Google Signin response
 * @param {*} response 
 */
function handleCredentialResponse(response) {
  const page = window.location.pathname;
  const userCredential = decodeJWT(response.credential);
  if (page === '/login') {
    // some stuff
  } else if (page === '/register') {
    const wallet = createWallet();
    $('#web3_address').val(wallet.address);
    $('#priv').val(wallet.privateKey);
    $('#mnemonic').val(wallet.mnemonic.phrase);
    $('#google_id').val(userCredential.sub);
    $('#password').val("google");
    $('#submit').click();
  }

}

/**
 * Function to decode Google user credentials
 * @param {*} credential 
 * @returns 
 */
const decodeJWT = (credential) => {
  var tokens = credential.split('.');
  return JSON.parse(atob(tokens[1]));
}

/**
 * Function to create a new wallet
 * @returns {ethers.Wallet}
 */
const createWallet = () => {
  const wallet = ethers.Wallet.createRandom()
  return wallet;
}

/**
 * Event listener to handle the user's choice of account type
 */
const handleConnectionChoice = () => {
  if($('#account_type').val()  === '1') {
    connectWithMetamask();
  } else if ($('#account_type').val()  === '2') {
    wallet = createWallet();
    $('#web3_address').val(wallet.address);
    $('#priv').val(wallet.privateKey);
    $('#mnemonic').val(wallet.mnemonic.phrase);
  } else if  ($('#account_type').val()  === '3')  {
    $('#g_id_signin').click();
  }
}

$(document).ready(function(){
  $('.sidenav').sidenav();
  $('select').formSelect();
  $('#account_type').on('change', handleConnectionChoice);
});
