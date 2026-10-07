import test from 'node:test';
import assert from 'node:assert/strict';
import {filterAssets,filterLoans} from './filters.js';
const assets=[{id:1,name:'Arduino kit',asset_tag:'LAB-001',category:'Electronics',available:2},
  {id:2,name:'Camera',asset_tag:'LAB-002',category:'Media',available:0},
  {id:3,name:'Multimeter',asset_tag:'LAB-003',category:'Electronics',available:0}];
test('only available equipment can be selected by the availability filter',()=>assert.deepEqual(filterAssets(assets,{availableOnly:true}).map(a=>a.id),[1]));
test('category and availability constraints compose',()=>assert.deepEqual(filterAssets(assets,{category:'Media',availableOnly:true}),[]));
test('case insensitive asset tag search',()=>assert.equal(filterAssets(assets,{search:' lab-002 '})[0].name,'Camera'));
test('name search composes with category',()=>assert.deepEqual(filterAssets(assets,{search:'camera',category:'Electronics'}),[]));
test('empty query preserves input and does not mutate inventory',()=>{const snapshot=JSON.stringify(assets);assert.equal(filterAssets(assets).length,3);assert.equal(JSON.stringify(assets),snapshot)});
test('history searches borrowers and equipment, retaining completed returns',()=>{const loans=[{asset_name:'Camera',borrower:'Demo Mira',returned_at:'2026-10-07'}];assert.equal(filterLoans(loans,'mIrA').length,1);assert.equal(filterLoans(loans,'camera').length,1);assert.equal(filterLoans(loans,'unknown').length,0)});
