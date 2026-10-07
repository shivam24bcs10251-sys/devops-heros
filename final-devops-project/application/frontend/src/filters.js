// Queries compose: a selected category never disables the availability constraint.
export function filterAssets(assets,{category='All',search='',availableOnly=false}={}) {
  const query=search.trim().toLowerCase();
  return assets.filter(asset => (category==='All'||asset.category===category)
    && (!availableOnly||asset.available>0)
    && `${asset.name} ${asset.asset_tag}`.toLowerCase().includes(query));
}
export function filterLoans(loans,search='') {
  const query=search.trim().toLowerCase();
  return loans.filter(loan=>`${loan.asset_name} ${loan.borrower}`.toLowerCase().includes(query));
}
