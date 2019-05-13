#author: Paulo Henrique Junqueira Amorim

def table(text):
    #to disable interpolation
    css = '<style type="text/css">\
            img { image-rendering: optimizeSpeed;\
            image-rendering: -moz-crisp-edges;\
            image-rendering: -o-crisp-edges;\
            image-rendering: -webkit-optimize-contrast;\
            image-rendering: pixelated;\
            image-rendering: optimize-contrast;\
            -ms-interpolation-mode: nearest-neighbor;} </style>\n'


    table_start = '<table style="width:100%">'
    table_end = '</table>'

    return '<body>' + table_start + '\n' +\
            css + text + table_end + '\n'\
            '</body>'

def row(text):

    row_start = '<tr>'
    row_end = '</tr>'

    return row_start + '\n' + text + row_end + '\n'

def cell(img_path):

    cell_start = '<td>'
    cell_end = '</td>'

    img = '<img src="' + img_path + '" height="42" width="42">'

    return cell_start + '\n' + img + cell_end + '\n'

