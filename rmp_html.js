javascript:(function(){
  const html = '<!DOCTYPE html>\n' + document.documentElement.outerHTML;
  const blob = new Blob([html], {type: 'text/html;charset=utf-8'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'rmp_rendered.html';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
})();